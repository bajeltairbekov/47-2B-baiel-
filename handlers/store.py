from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot


class Store(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    photo = State()


# Старт FSM
async def start_fsm(message: types.Message):
    await message.answer('Введите название продукта:')
    await Store.name.set()


# Обработка имени
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton(text='S')
    b2 = KeyboardButton(text='M')
    b3 = KeyboardButton(text='L')
    kb.add(b1, b2, b3)
    await message.answer('Укажите размер:', reply_markup=kb)
    await Store.size.set()


# Обработка размера
async def process_size(message: types.Message, state: FSMContext):
    if message.text not in ['S', 'M', 'L']:
        await message.answer('Выберите размер, используя кнопки ниже.')
        return

    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Укажите категорию:', reply_markup=types.ReplyKeyboardRemove())
    await Store.category.set()


# Обработка категории
async def process_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer('Укажите цену:')
    await Store.price.set()


# Обработка цены
async def process_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Цена должна быть числом. Попробуйте снова.')
        return

    async with state.proxy() as data:
        data['price'] = int(message.text)

    await message.answer('Загрузите фотографию:')
    await Store.photo.set()


# Обработка фотографии
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer('Пожалуйста, отправьте фотографию.')
        return

    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id  # Берем самое качественное фото

    # Отправляем подтверждение
    await message.answer(f"Продукт сохранен:\n"
                         f"Название: {data['name']}\n"
                         f"Размер: {data['size']}\n"
                         f"Категория: {data['category']}\n"
                         f"Цена: {data['price']} руб.\n"
                         f"Фотография: отправляется...")

    await bot.send_photo(chat_id=message.chat.id, photo=data['photo'])
    await state.finish()


# Регистрация хэндлеров
def register_store(dp: Dispatcher):
    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(process_name, state=Store.name)
    dp.register_message_handler(process_size, state=Store.size)
    dp.register_message_handler(process_category, state=Store.category)
    dp.register_message_handler(process_price, state=Store.price)
    dp.register_message_handler(process_photo, content_types=['photo'], state=Store.photo)
