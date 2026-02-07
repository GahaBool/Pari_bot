from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import os

ADMIN_IDS = [int(id_) for id_ in os.getenv("ADMIN_IDS", "").split(",") if id_]


def get_main_keyboard(user_id: int):

    if user_id in ADMIN_IDS:
    
        return ReplyKeyboardMarkup(
            keyboard=[
                # Первый ряд - основные функции
                [   
                    KeyboardButton(text="🎯 Активные события"),
                ],
                
                # Второй ряд - личный кабинет
                [
                    KeyboardButton(text="💰 Мой баланс"),
                    KeyboardButton(text="📊 Мои ставки"),
                ],

                # Ряд 1 - УПРАВЛЕНИЕ СОБЫТИЯМИ
                [
                    KeyboardButton(text="➕ Создать событие"),
                    KeyboardButton(text="📝 Завершить событие"),
                ],
                
                # Ряд 2 - УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
                [
                    KeyboardButton(text="💎 Начислить Ё-баллы"),
                    KeyboardButton(text="👥 Список пользователей"),
                ],
                
                # Ряд 4 - ВОЗВРАТ В МЕНЮ
                [
                    KeyboardButton(text="❓ Помощь и правила"),
                ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Админ-действия..."
        )

    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                # Первый ряд - основные функции
                [   
                    KeyboardButton(text="🎯 Активные события"),
                ],
                
                # Второй ряд - личный кабинет
                [
                    KeyboardButton(text="💰 Мой баланс"),
                    KeyboardButton(text="📊 Мои ставки"),
                ],
                
                # Третий ряд - информация
                [
                    KeyboardButton(text="❓ Помощь и правила"),
                ],
            ],

            resize_keyboard=True,
            input_fiеld_placeholder="Что вам интереует?",
        )


delete_keyboard = ReplyKeyboardRemove()

