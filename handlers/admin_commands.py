from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject
from filters.chat_types import ChatTypeFilter, IsAdmin

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards import reply

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

class CreateEvent(StatesGroup):
    #Состояние создание события
    waiting_for_title = State()          # Ждем название
    waiting_for_description = State()    # Ждем описание

class DeleteEvent(StatesGroup):
    #Состояние закрытия события
    waiting_for_id = State()    #Ожидание ID

class AddCoins(StatesGroup):
    #Начисление балоов пользователю
    waiting_for_user_id = State() #Ожидание ID
    waiting_for_coins = State() #Ожидание колличество баллов

class AddUsers(StatesGroup):
    waiting_for_add_user = State() #Ожидание ID

class DeleteUsers(StatesGroup):
    waiting_for_delete_user = State() #Ожидание ID
    

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

#<------------------------Завершение события--------------------------->
# /closeevent - Завершить событие
@admin_router.message(F.text == "📝 Завершить событие")
@admin_router.message(Command("closeevent"))
async def close_event_command(message: types.Message, state: FSMContext):
    await message.answer(
        "📝 <b>Завершить событие</b>\n\n"
        "Введите ID события:",
        reply_markup=reply.cancel_back)
    await state.set_state(DeleteEvent.waiting_for_id)

@admin_router.message(DeleteEvent.waiting_for_id)
async def delete_event_for_id(message: types.Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer("❌ Необходимо ввести ID (только цифры)")
        return
    
    await state.update_data(event_id=message.text)
    
    event_id = int(message.text)
    await message.answer(f"✅ Событие #{event_id} удалено!", reply_markup=reply.get_main_keyboard(message.from_user.id))
    # Очищаем состояние
    await state.clear()

#<------------------------------------------------------------------------------>

#<------------------------Начисление баллов--------------------------->
# /addcoins - Начислить Ё-баллы  
@admin_router.message(F.text == "💎 Начислить Ё-баллы")
@admin_router.message(Command("addcoins"))
async def add_coins_command(message: types.Message, state: FSMContext):
    await message.answer(
        "💎  <b>Начислить Ё-баллы</b>\n\n"
        "Введите ID пользователя:",
        reply_markup=reply.cancel_back)
    await state.set_state(AddCoins.waiting_for_user_id)

@admin_router.message(AddCoins.waiting_for_user_id)
async def add_coins_for_id(message: types.Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("❌ Необходимо ввести ID (только цифры)")
        return
    
    await state.update_data(user_id=message.text)
    await message.answer("Введите колличество Ё-баллов(В формате: 1000):", reply_markup=reply.cancel_back)
    await state.set_state(AddCoins.waiting_for_coins)

@admin_router.message(AddCoins.waiting_for_coins)
async def add_count_coins(message: types.Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("❌ Необходимо ввести только сумму балов (только цифры)")
        return

    await state.update_data(coins_count=message.text)

    count_coins = message.text
    await message.answer(f"{count_coins} Баллы успешно добавлены!", reply_markup=reply.get_main_keyboard(message.from_user.id))
    
    # Очищаем состояние
    await state.clear()

#<------------------------------------------------------------------------------>

#<------------------------Добавление/Удаление пользователей--------------------------->
# /users - Добавление пользователя
@admin_router.message(F.text == "👤➕ Добавить пользователя")
@admin_router.message(Command("add_user"))
async def add_users_command(message: types.Message, state: FSMContext):
    await message.answer(
        "👤➕ <b>Добавить пользователя</b>\n\n"
        "Введите ID пользователя которого необходимо добавить:",
        reply_markup=reply.cancel_back)
    await state.set_state(AddUsers.waiting_for_add_user)

@admin_router.message(AddUsers.waiting_for_add_user)
async def add_event_for_id(message: types.Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer("❌ Необходимо ввести ID пользователя (только цифры)")
        return
    
    await state.update_data(user_id=message.text)
    
    user_id = int(message.text)
    await message.answer(f"✅ Пользователь с ID: {user_id} добавлен!", reply_markup=reply.get_main_keyboard(message.from_user.id))
    # Очищаем состояние
    await state.clear()


# Удаление пользвателя 
@admin_router.message(F.text == "👤➖ Удалить пользователя")
@admin_router.message(Command("ban_user"))
async def delete_users_command(message: types.Message, state: FSMContext):
    await message.answer(
        "👤➕ <b>Добавить пользователя</b>\n\n"
        "Введите ID пользователя которого необходимо добавить:",
        reply_markup=reply.cancel_back)
    await state.set_state(DeleteUsers.waiting_for_delete_user)

@admin_router.message(DeleteUsers.waiting_for_delete_user)
async def delete_user_for_id(message: types.Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer("❌ Необходимо ввести ID пользователя (только цифры)")
        return
    
    await state.update_data(user_id=message.text)
    
    user_id = int(message.text)
    await message.answer(f"✅ Пользователь с ID: {user_id} удален!", reply_markup=reply.get_main_keyboard(message.from_user.id))
    # Очищаем состояние
    await state.clear()
#<------------------------------------------------------------------------------>


