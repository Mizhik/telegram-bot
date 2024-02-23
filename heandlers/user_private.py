import os
from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy.ext.asyncio import AsyncSession

import requests
import json

import webbrowser
from database.orm_query import orm_get_products
from filters.chat_types import ChatTypeFilter

from kbds import reply
from kbds.reply import get_keyboard


user_private_router = Router()
API = api=os.getenv("API")
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(
        "Hello, i'm virtual support",
        reply_markup=get_keyboard(
            'Menu',
            'Creator',
            'Payment',
            'Shipping',
            placeholder="What do you want?",
            sizes=(2,2)
        ),
    )
#при вписуванні слів визначених слів або іншого
# @user_private_router.message()
# async def echo(message: types.Message):
#     text = message.text

#     if text.lower() in ["hi"]:
#         await message.answer("Hello@")
#     elif text.lower() in ["bay"]:
#         await message.answer("Bay@")
#     else:
#         await message.answer('@'+message.from_user.username)

@user_private_router.message(Command("github"))
async def me_gitgub(message):
    webbrowser.open("https://github.com/Mizhik/telegram-bot")

@user_private_router.message(or_f(Command("creator"),(F.text.lower()=='creator')))
async def about_me(message: types.Message):
    await message.answer_photo(photo=types.FSInputFile('./photo.jpeg'))
    await message.answer("I'a Vlad\n19 years old\nKiev")


@user_private_router.message(or_f(Command("menu"),(F.text.lower()=="menu")))
async def menu_bot(message: types.Message, session:AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}\
                    </strong>\n{product.description}\nЦіна: {round(product.price,2)}',
        )
    await message.answer("Меню:")

@user_private_router.message((F.text.lower() == 'варіанти оплати') | (F.text.lower()=="payment"))
@user_private_router.message(Command("payment"))
async def payment_bot(message: types.Message):

    text = as_marked_section(
        Bold("Варіанти оплати:"),
        "Карткою в боті",
        "При отриманні картка/готівка",
        "У закладі",
        marker="✅ "
    )
    await message.answer(text.as_html())
    
@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варіанти доставки") | (F.text.lower()=="shipping"))
@user_private_router.message(Command("shipping"))
async def payment_bot(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варіанти доставки/замовлення:"),
            "Кур'єр",
            "Самовивіз",
            "У закладі",
            marker="✅ "
        ),
        as_marked_section(
            Bold("Неможна:"),
            "Почта",
            "Голубом",
            marker="🚫 "
        ),
        sep='\n--------------------------\n'
    )
    await message.answer(text.as_html())

@user_private_router.message(Command("weather"))
async def weather(message: types.Message):
    await message.answer("Enter name your city:")
    @user_private_router.message()
    async def result(message):
        city = message.text
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        if res:
            data = json.loads(res.text)
            temp = data['main']['temp']

            photo=types.FSInputFile("sun.jpg" if temp > 5.0 else 'snow.jpg')
            #image = "sun.jpg" if temp > 5.0 else 'snow.jpg'
            await message.answer_photo(photo)
            await message.reply(f"Now weather: {temp}")
        else:
            await message.reply(f"{city} - Сity does not exist",reply_markup=get_keyboard)

@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer("Номер отримано")
    await message.answer(str(message.contact))

@user_private_router.message(F.location)
async def get_contact(message: types.Message):
    await message.answer("Локацію отримано")
    await message.answer(str(message.location))