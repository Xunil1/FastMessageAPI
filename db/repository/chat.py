from typing import List, Dict, Any
from uu import decode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException

from db.models.chat import Chat
from db.models.user import User
from db.repository.user import user_view


async def chat_view(chat: Chat) -> Dict[str, Any]:
    return {
        "id": chat.id,
        "members": [await user_view(user) for user in chat.users]
    }


async def create_new_chat(members: list, db: AsyncSession):
    if members is None or len(members) < 2:
        raise HTTPException(status_code=400, detail="Inccorect number of members")

    user_list: List[User] = []

    for member in members:
        result = await db.execute(select(User).where(User.username == member))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        user_list.append(user)

    chat = Chat()
    for user in user_list:
        chat.users.append(user)

    db.add(chat)
    await db.commit()
    await db.refresh(chat)


async def get_chats_by_username(username: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    chat_list = list()
    for chat in user.chats:
        chat_list.append(chat.id)

    return {"chats": chat_list}

async def get_chat_by_id(chat_id: int, db: AsyncSession):
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalars().first()
    if chat is None:
        raise HTTPException(status_code=400, detail="Chat not found")
    return await chat_view(chat)



