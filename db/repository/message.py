from datetime import datetime
from typing import Dict, Any

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException

from db.models.chat import Chat
from db.models.user import User

from db.models.message import Message

async def message_view(message: Message) -> Dict[str, Any]:
    return {
        "sender": message.sender.username,
        "message": message.message,
        "date": message.send_time.strftime("%Y-%m-%d %H:%M:%S"),
    }


async def add_message(chat_id: int, sender: str, msg: str, db: AsyncSession):
    # Проверка чата
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalars().first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Проверка отправителя
    result = await db.execute(select(User).where(User.username == sender))
    s_user = result.scalars().first()
    if s_user is None and s_user in chat.users:
        raise HTTPException(status_code=403, detail="Access denied")

    # Проверка получателя
    r_user = None
    for member in chat.users:
        if member.username != sender:
            r_user = member

    if r_user is None:
        raise HTTPException(status_code=404, detail="User not found")



    message = Message(sender_id=s_user.id, chat_id=chat.id, message=msg, send_time=datetime.now())
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return {
        "message": await message_view(message),
        "receiver": r_user.username,
    }

async def get_history_by_chat_id(chat_id: id, sender: str, offset: int, limit: int, db: AsyncSession):
    result = await db.execute(select(Message).where(Message.chat_id == chat_id).order_by(desc(Message.send_time)))
    messages = result.scalars().all()

    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalars().first()

    if all(map(lambda user: user.username != sender, chat.users)):
        raise HTTPException(status_code=403, detail="Access denied")

    message_history = list()
    for message in messages:
        message_history.append(await message_view(message))

    return {"history": message_history[offset:offset + limit]}





