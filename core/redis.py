import aioredis
from core.config import settings


redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def set_user_online(username: str):
    key = f"user:{username}:online"
    await redis.setnx(key, "online") # Добавление ключа в Redis

async def is_user_online(username: str) -> bool:
    key = f"user:{username}:online"
    return await redis.exists(key) == 1  # Если ключ существует, пользователь онлайн

async def set_user_offline(username: str):
    key = f"user:{username}:online"
    await redis.delete(key)  # Удаление ключа из Redis