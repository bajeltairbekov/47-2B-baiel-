from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from random import choice


games = ["🏀", "🎲", "🎯", "🎰", "🎳"]


async def game(message: types.Message):
    game = choice(games)
    await bot.send_dice(
        emoji=game,
        chat_id=message.from_user.id
    )


def register_game(dp: Dispatcher):
    dp.register_message_handler(game, commands=['game_dice'])
