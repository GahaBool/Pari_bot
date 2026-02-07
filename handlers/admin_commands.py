from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject
from filters.chat_types import ChatTypeFilter, IsAdmin

from keyboards import reply

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

#<------------------------Меню админа и обычное меню--------------------------->
@admin_router.message(Command("admin"))
async def admin_command(message: types.Message):
    # Простая проверка
    await message.answer("👋 Привет админ!", reply_markup=reply.get_main_keyboard(message.from_user.id))
#<------------------------_----------------------------------------------------->


# /addevent - Создать событие
@admin_router.message(Command("addevent"))
async def add_event_command(message: types.Message):
    await message.answer("➕ Введите название нового события:", reply_markup=reply.reply.delete_keyboard)

# /closeevent - Завершить событие
@admin_router.message(Command("closeevent"))
async def close_event_command(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"📝 Завершаю событие #{command.args}")
    else:
        await message.answer("❌ Укажите ID события: /closeevent 123", reply_markup=reply.reply.delete_keyboard)

# /addcoins - Начислить Ё-баллы  
@admin_router.message(Command("addcoins"))
async def add_coins_command(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"💎 Начисляю баллы: {command.args}", reply_markup=reply.reply.delete_keyboard)
    else:
        await message.answer("❌ Формат: /addcoins user_id сумма" , reply_markup=reply.reply.delete_keyboard)

# /statsall - Статистика системы
@admin_router.message(Command("statsall"))
async def stats_all_command(message: types.Message):
    await message.answer("📊 Статистика загружается...", reply_markup=reply.reply.delete_keyboard)

# /users - Список пользователей
@admin_router.message(Command("users"))
async def users_command(message: types.Message):
    await message.answer("👥 Список пользователей загружается...", reply_markup=reply.delete_keyboard)
# Простой текст как запасной вариант
@admin_router.message(F.text == "Админ")
async def admin_text_command(message: types.Message):
    await message.answer(
        "Админ команды:\n"
        "/addevent - Создать событие\n"
        "/closeevent - Завершить событие\n"  
        "/addcoins - Начислить баллы\n"
        "/statsall - Статистика\n"
        "/users - Пользователи", reply_markup=reply.reply.delete_keyboard
    )