import os
from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
import webbrowser
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Hello, i'm virtual support")

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

@user_private_router.message(Command("creator"))
async def about_me(message: types.Message):
    await message.answer_photo(photo=types.FSInputFile('./photo.jpeg'))
    await message.answer("I'a Vlad\n19 years old\nKiev")


@user_private_router.message(or_f(Command("menu"),(F.text.lower()=="меню")))
async def menu_bot(message: types.Message):
    await message.answer("Меню:\n1.\n2.\n3.")

@user_private_router.message(F.text.lower() == 'варіанти оплати')
@user_private_router.message(Command("payment"))
async def payment_bot(message: types.Message):
    await message.answer("Варіанти оплати:\n-\n-\n-")

@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "варіанти доставки"))
@user_private_router.message(Command("shipping"))
async def payment_bot(message: types.Message):
    await message.answer("Варіанти доставки:\n-\n-\n-")

