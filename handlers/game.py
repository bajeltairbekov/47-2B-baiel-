from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot

game = [1, 2, 3, 4, 5, 6]


async def game(message: types.Message):
    await bot.send_dice(
        emoji=game,
        chat_id=message.from_user.id
    )


def register_game(dp: Dispatcher):
    dp.register_message_handler(game, commands=['game_dice'])
