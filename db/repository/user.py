from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException

from db.models.user import User

from schemas.user import UserCreate

from core.redis import is_user_online

from core.jwt_token import verify_jwt_token
from core.hashing import Hasher
from core.jwt_token import create_jwt_token, EXPIRATION_TIME


async def user_view(user: User) -> Dict[str, Any]:
    status = await is_user_online(user.username)
    return {
        "id": user.id,
        "username": user.username,
        "status": "online" if status else "offline",
    }


async def auth_current_user(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = Hasher.verify_password(password, user.hash_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if user.token and verify_jwt_token(user.token):
        return {"access_token": user.token, "token_type": "bearer"}

    jwt_token = create_jwt_token({
        "exp": EXPIRATION_TIME,
        "username": user.username,
    })

    user.token = jwt_token
    await db.commit()

    return {"access_token": jwt_token, "token_type": "bearer"}


async def create_new_user(user_c: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == user_c.username))
    user = result.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail="Username and password already exists")
    if len(user_c.password) == 0:
        raise HTTPException(status_code=400, detail="Password can not be empty")
    elif len(user_c.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    user = User(username=user_c.username, hash_password=Hasher.get_password_hash(user_c.password))
    db.add(user)
    await db.commit()  # Подтверждаем изменения
    await db.refresh(user)  # Обновляем объект, чтобы получить сгенерированный ID
    return await user_view(user)


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    result = list()
    for user in users:
        result.append(await user_view(user))
    return {"users": result}


async def link_by_tg(username: str, tg_id: int, db: AsyncSession ):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user.telegram_id = tg_id
    await db.commit()
    await db.refresh(user)
    return {"status": "ok", "detail": "Профиль мессенджера успешно связан"}

async def get_user_tg_id(username: str, db: AsyncSession ):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    await db.commit()
    return {"tg_id": user.telegram_id}