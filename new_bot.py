import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart,Command
from aiogram.types import InputFile


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


from heandlers.user_private import user_private_router
from heandlers.user_group import user_group_router
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message,edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    #await bot.delet_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot,allowed_updates= ALLOWED_UPDATES)

asyncio.run(main())