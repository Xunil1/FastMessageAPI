from email.policy import default
from typing import List, Dict, Any
from uu import decode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

from fastapi import HTTPException

from db.models.chat import Chat
from db.models.user import User
from db.models.user_chat import UserChat
from db.repository.user import user_view


async def chat_view(chat: Chat) -> Dict[str, Any]:
    return {
        "id": chat.id,
        "members": [await user_view(user) for user in chat.users]
    }


async def create_new_chat(members: list, db: AsyncSession):
    if members is None or len(members) != 2:
        raise HTTPException(status_code=400, detail="Inccorect number of members")

    user_list: List[User] = []

    for member in members:
        result = await db.execute(select(User).where(User.username == member))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        user_list.append(user)

    u1_chats = set(user_list[0].chats)
    u2_chats = set(user_list[1].chats)

    if not u1_chats.isdisjoint(u2_chats):
        raise HTTPException(status_code=400, detail="Chat already exists")

    chat = Chat()
    for user in user_list:
        chat.users.append(user)
    db.add(chat)

    await db.commit()
    await db.refresh(chat)

    return {"id": chat.id}


async def get_all_chats(username: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    chat_list: List[Chat] = list()
    for chat in user.chats:
        await db.refresh(chat)
        chat_list.append(chat.id)

    return {"chats": chat_list}

async def get_chat_info_by_chat_id(chat_id: int, db: AsyncSession):
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalars().first()

    if chat is None:
        raise HTTPException(status_code=400, detail="Chat not found")

    await db.commit()
    await db.refresh(chat)

    return await chat_view(chat)


async def get_chat_by_members(members: list, db: AsyncSession):
    if members is None or len(members) != 2:
        raise HTTPException(status_code=400, detail="Inccorect number of members")

    member1_chats = await get_all_chats(members[0], db)
    member2_chats = await get_all_chats(members[1], db)

    set_member1_chats = set(member1_chats["chats"])
    set_member2_chats = set(member2_chats["chats"])


    if set_member1_chats.isdisjoint(set_member2_chats):
        raise HTTPException(status_code=400, detail="Chat not found")


    chat_id = set_member1_chats.intersection(set_member2_chats).pop()

    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalars().first()


    await db.commit()
    await db.refresh(chat)

    return {"id": chat.id}
