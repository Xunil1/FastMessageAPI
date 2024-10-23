from typing import Union
from fastapi import APIRouter, WebSocket, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from core.connection_manager import manager, Username
from core.jwt_token import verify_jwt_token
from core.redis import set_user_online, set_user_offline
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from db.repository.message import add_message, get_history_by_chat_id
from db.repository.user import get_user_tg_id
from db.session import get_db


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, db: AsyncSession = Depends(get_db)):
    username = Username(username)
    await manager.connect(username, websocket)
    await set_user_online(username)
    await manager.broadcast_send({"type": "user_status", "detail":{"username": username, "status": "online"}})

    try:
        while True:
            data = await websocket.receive_json()

            try:
                res = await add_message(
                    chat_id=int(data["chat_id"]),
                    sender=data["username"],
                    msg=data["message"],
                    db=db,
                )
            except HTTPException as ex:
                await websocket.send_json({"type": "error", "status_code": ex.status_code, "detail": ex.detail})
            else:
                tg_id = await get_user_tg_id(username=res["receiver"], db=db)
                await manager.send_json(username, {"type": "ok", "status_code": 200,  "detail": "sended", "msg": res["message"]})
                await manager.send_json(res["receiver"], {"type": "message", "sender": username, "msg": res["message"]}, tg_id=tg_id["tg_id"])





    except WebSocketDisconnect:

        await manager.disconnect(username)
        await set_user_offline(username)


@router.get("/{chat_id}")
async def get_history(chat_id: int, offset: int = 0, limit: int = 10, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    data = await get_history_by_chat_id(chat_id=chat_id, sender=token_data["username"], offset=offset, limit=limit, db=db)
    return data