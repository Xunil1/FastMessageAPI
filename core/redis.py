import aioredis
from datetime import timedelta


redis = aioredis.from_url("redis://localhost:6379", decode_responses=True)

async def set_user_online(username: str):
    key = f"user:{username}:online"
    await redis.setex(key, timedelta(minutes=5), "online")  # Статус хранится 10 минут

async def is_user_online(username: str) -> bool:
    key = f"user:{username}:online"
    return await redis.exists(key) == 1  # Если ключ существует, пользователь онлайн

async def set_user_offline(username: str):
    key = f"user:{username}:online"
    await redis.delete(key)  # Удаление ключа из Redis

async def refresh_user_status(username: str):
    key = f"user:{username}:online"
    await redis.expire(key, timedelta(minutes=5))  # Обновление времени жизни статуса