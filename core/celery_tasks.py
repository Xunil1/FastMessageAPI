from celery import Celery
import asyncio
from core.config import settings

app = Celery('core', broker=settings.REDIS_URL + '/2')

@app.task()
def send_notify(chat_id: int, notify_message: dict):
    asyncio.run(notify(chat_id=chat_id, message=f'Вам пришло новое сообщение от : {notify_message["msg"]["sender"]}\nТекст сообщения: {notify_message["msg"]["message"]}'))


async def notify(chat_id: int, message: str):
    import aiogram
    bot = aiogram.Bot(token='6556471168:AAHbSPqzi9xWJDVc4iH5NnqB8IvA-n7MDds')
    await bot.send_message(chat_id, message)