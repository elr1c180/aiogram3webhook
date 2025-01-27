from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_bot() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Покупка материалов", callback_data="buy_course")
    kb.button(text="Отзывы", callback_data="reviews")
    kb.adjust(1)
    return kb.as_markup()