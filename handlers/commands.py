from aiogram import types, Dispatcher
from config import bot, dp

import os


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}\n'
                                f'Твой Telegram Id - {message.from_user.id}')

async def mem(message: types.Message):
    photo = open('media/png.jpeg','rb')
    await bot.send_photo(
        photo=photo,
        chat_id=message.from_user.id
    )

def register_commands(dp:Dispatcher):
    dp.register_message_handler(start,commands=['start'])
    dp.register_message_handler(mem, commands=['mem'])