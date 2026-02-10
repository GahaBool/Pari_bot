import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from database.engine import create_db, drop_db

from handlers.user_commands import user_router
from handlers.admin_commands import admin_router

from common.bot_cmds_list import user_commands_menu

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('token'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)

async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('The bot does not respond to requests!')

async def main():
    dp.startup.register(on_startup)
    dp.startup.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=user_commands_menu, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())