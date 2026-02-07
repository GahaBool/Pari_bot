from aiogram import  F, types, Router
from aiogram.filters import CommandStart, Command
from filters.chat_types import ChatTypeFilter

from keyboards import reply

from .texts_answer import welcome_txt

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))

@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(welcome_txt, reply_markup=reply.get_main_keyboard(message.from_user.id))

@user_router.message(F.text == "📱 Главное меню")
@user_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer(welcome_txt, reply_markup=reply.get_main_keyboard(message.from_user.id))

@user_router.message(F.text == '🎯 Активные события')
async def start_cmd(message: types.Message):
    await message.answer(welcome_txt, reply_markup=reply.get_main_keyboard(message.from_user.id))

@user_router.message(F.text == '💰 Мой баланс')
async def start_cmd(message: types.Message):
    await message.answer(welcome_txt, reply_markup=reply.get_main_keyboard(message.from_user.id))

@user_router.message(F.text == '📊 Мои ставки')
async def _cmd(message: types.Message):
    await message.answer(welcome_txt, reply_markup=reply.get_main_keyboard(message.from_user.id))

@user_router.message(Command('help'))
@user_router.message(F.text == '❓ Помощь и правила')
async def help_cmd(message: types.Message):
    await message.answer(welcome_txt, reply_markup=reply.delete_keyboard)




    





