import os
from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import InputFile
import webbrowser

user_private_router = Router()

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
    await webbrowser.open("https://github.com/Mizhik/telegram-bot")


@user_private_router.message(Command("menu"))
async def menu_bot(message):
    await message.answer("Menu:\n1.\n2.\n3.")

@user_private_router.message(Command("creator"))
async def about_me(message):
    await message.answer_photo(photo=types.FSInputFile('./photo.jpeg'))
    await message.answer("I'a Vlad\n19 years old\nKiev")

