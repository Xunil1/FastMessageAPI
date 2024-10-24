from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.jwt_token import verify_jwt_token
from core.types.types import Username
from db.session import get_db
from db.repository.chat import create_new_chat, get_chat_info_by_chat_id, get_all_chats, get_chat_by_members


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")

@router.post("/{username}")
async def create_chat(username: str, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    data = await create_new_chat(members=[Username(username), token_data["username"]], db=db)
    return data

@router.get("/id/{username}")
async def get_chat(username: str, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    data = await get_chat_by_members(members=[Username(username), token_data["username"]], db=db)
    return data

@router.get("/info")
async def get_chat_info(chat_id: int, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    data = await get_chat_info_by_chat_id(chat_id=chat_id, db=db)
    return data

@router.get("/")
async def get_chats(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    data = await get_all_chats(username=token_data["username"], db=db)
    return data