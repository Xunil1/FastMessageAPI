from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.jwt_token import verify_jwt_token
from typing import Annotated, Union

from db.models.user import User

from schemas.user import UserCreate
from db.session import get_db
from db.repository.user import auth_current_user, create_new_user, get_all_users, link_by_tg


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


@router.post("/auth")
async def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    data = await auth_current_user(form_data.username, form_data.password, db=db)
    return data

@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    data = await create_new_user(user_c=user, db=db)
    return data

@router.get("/")
async def get_users(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    data = await get_all_users(db=db)
    return data

@router.post("/link/tg/{tg_id}")
async def create_user(tg_id: int, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = verify_jwt_token(token)
    if token_data is None:
        raise HTTPException(status_code=403, detail="Неверный токен")
    data = await link_by_tg(username=token_data["username"], tg_id=tg_id, db=db)
    return data

