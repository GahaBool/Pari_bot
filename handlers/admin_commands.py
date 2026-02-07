from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject
from filters.chat_types import ChatTypeFilter, IsAdmin

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards import reply

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

class CreateEvent(StatesGroup):
    waiting_for_title = State()          # Ждем название
    waiting_for_description = State()    # Ждем описание

#<------------------------Меню админа и обычное меню--------------------------->
@admin_router.message(F.text == "📱 Главное меню")
@admin_router.message(Command('menu'))
async def admin_command(message: types.Message):
    # Простая проверка
    await message.answer(f"👋 Привет Админ!", reply_markup=reply.get_main_keyboard(message.from_user.id))
#<------------------------------------------------------------------------------>

#<------------------------Панель отмены и назад--------------------------->
@admin_router.message(Command("cancellation"))
@admin_router.message(F.text == "❌ Отмена")
async def cancel_create_event(message: types.Message, state: FSMContext):
    """Отмена создания события"""
    await state.clear()
    await message.answer(
        "❌ Создание события отменено",
        reply_markup=reply.get_main_keyboard(message.from_user.id)  # Возвращаем админ-меню
    )

@admin_router.message(Command("back"))
@admin_router.message(F.text == "🔙 Назад")
async def back_in_create_event(message: types.Message, state: FSMContext):
    """Возврат на предыдущий шаг"""
    current_state = await state.get_state()
    
    if current_state == CreateEvent.waiting_for_description:
        await message.answer("Введите название события:")
        await state.set_state(CreateEvent.waiting_for_title)
    elif current_state == CreateEvent.waiting_for_options:
        await message.answer("Введите описание события:")
        await state.set_state(CreateEvent.waiting_for_description)
    else:
        await message.answer("Нельзя вернуться дальше")

#<------------------------------------------------------------------------------>

#<------------------------Создание события--------------------------->
@admin_router.message(F.text == "➕ Создать событие")
@admin_router.message(Command("addevent"))
async def add_event_command(message: types.Message, state: FSMContext):
    await message.answer(
        "🎯 <b>Создание нового события</b>\n\n"
        "Введите название события:",
        reply_markup=reply.cancel_back)
    await state.set_state(CreateEvent.waiting_for_title)

@admin_router.message(CreateEvent.waiting_for_title)
async def add_event_command(message: types.Message, state: FSMContext):

    if len(message.text) < 5:
        await message.answer("❌ Название должно быть не менее 5 символов")
        return
    
    await state.update_data(title=message.text)

    await message.answer("Введите описание нового события:", reply_markup=reply.cancel_back)

    await state.set_state(CreateEvent.waiting_for_description)


@admin_router.message(CreateEvent.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    """Обрабатываем описание события"""
    if len(message.text) < 10:
        await message.answer("❌ Описание должно быть не менее 10 символов")
        return
    
    await state.update_data(description=message.text)

# Отправляем подтверждение
    await message.answer(
        f"✅ <b>Событие создано успешно!</b>\n\n"
        f"📋 <b>ID события:</b>\n\n"
        f"🎯 <b>Название:</b>\n\n"
        f"📝 <b>Описание:</b>\n\n"
        f"📊 <b>Коэффициенты:</b> ЗА  | ПРОТИВ ",
        reply_markup=reply.get_main_keyboard(message.from_user.id),  # Возвращаем админ-панель
        parse_mode="HTML"
    )
    
    # Очищаем состояние
    await state.clear()

#<------------------------------------------------------------------------------>

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