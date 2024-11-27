from aiogram import executor, types
from config import dp
from handlers import commands, quiz, game, store
from aiogram.contrib.fsm_storage.memory import MemoryStorage


quiz.register_handler_quiz(dp)
commands.register_commands(dp)
game.register_game(dp)
store.register_store(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
