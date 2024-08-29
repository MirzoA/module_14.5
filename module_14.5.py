from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button1)
kb.add(button2)
kb.add(button3)
kb.add(button4)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(inline_button)
inline_kb.add(inline_button2)


inline_kb_2 = InlineKeyboardMarkup(resize_keyboard=True)
inline_button_1 = InlineKeyboardButton(text='Клей для пенополистирола ZM-01', callback_data='product_buying1')
inline_button_2 = InlineKeyboardButton(text='Клей для плитки ZM-51', callback_data='product_buying2')
inline_button_3 = InlineKeyboardButton(text='Клей для блоков ZM-22', callback_data='product_buying3')
inline_button_4 = InlineKeyboardButton(text='Штукатурка гладкая цементно-известковая ZM-41', callback_data='product_buying4')
inline_kb_2.add(inline_button_1)
inline_kb_2.add(inline_button_2)
inline_kb_2.add(inline_button_3)
inline_kb_2.add(inline_button_4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Формула Миффлина-Сан Жеора – это формула расчета калорий для '
                         'оптимального похудения или сохранения нормального веса.')

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    db = get_all_products()
    for i in range(0, 4):
        await message.answer(f'Название: {db[i][0]} | Описание: {db[i][1]}| Цена: {db[i][2]}')
        with open(f'{i}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:',reply_markup=inline_kb_2)


@dp.callback_query_handler(text='product_buying1')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели клей для пенополистирола ZM-01')
    await call.answer()

@dp.callback_query_handler(text='product_buying2')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели клей для плитки ZM-51')
    await call.answer()

@dp.callback_query_handler(text='product_buying3')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели клей для блоков ZM-22')
    await call.answer()

@dp.callback_query_handler(text='product_buying4')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели штукатурку гладкую цементно-известковую ZM-41')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_man = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий {result_man} день')
    await state.finish()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Регистрация прошла успешно!', reply_markup=kb)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
