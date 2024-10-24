import os
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import asyncio
import aiohttp

from states.auth_state import AuthStates

BACKEND_IP = os.getenv("BACKEND_IP")
BACKEND_PORT = os.getenv("BACKEND_PORT")
API_TOKEN = os.getenv("API_TOKEN")
AUTH_URL = f'http://{BACKEND_IP}:{BACKEND_PORT}/user/auth'
LINK_URL = f'http://{BACKEND_IP}:{BACKEND_PORT}/user/link/tg'

if BACKEND_IP is None or BACKEND_PORT is None or API_TOKEN is None:
    print("Требуется токен и адрес Back-end части.")
    exit()


bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

users = {}

@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Введите ваш логин:")
    await state.set_state(AuthStates.waiting_for_username)


@dp.message(AuthStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Теперь введите ваш пароль:")
    await state.set_state(AuthStates.waiting_for_password)


@dp.message(AuthStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get('username')
    password = message.text
    user_id = message.from_user.id
    auth_res = await auth(username, password, user_id)
    if auth_res["status"]:
        link_res = await link(auth_res["detail"], user_id)
        if link_res["status"]:
            await message.answer(f"{link_res['detail']}")
        else:
            await message.answer(f"Ошибка: {link_res['detail']}")
            await message.answer(f"Пожалуйста, воспользуйтесь снова командой /start")
    else:
        await message.answer(f"Ошибка: {auth_res['detail']}")
        await message.answer(f"Пожалуйста, воспользуйтесь снова командой /start")
    await state.clear()


async def auth(username: str, password: str, user_id: int) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        try:
            payload = {"username": username, "password": password}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            async with session.post(AUTH_URL, data=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    status = True
                    detail = result.get("access_token")
                else:
                    error_message = await response.json()
                    status = False
                    detail = error_message["detail"]
        except aiohttp.ClientError as e:
            status = False,
            detail = "Не удалось подключиться к серверу"
    return {
        "status": status,
        "detail": detail
    }


async def link(token: str, tg_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            async with session.post(LINK_URL + f"/{tg_id}", headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    status = True
                    detail = result.get("detail")
                else:
                    error_message = await response.json()
                    status = False
                    detail = error_message["detail"]
        except aiohttp.ClientError as e:
            status = False
            detail = "Не удалось подключиться к серверу"

    return {
        "status": status,
        "detail": detail,
    }


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())