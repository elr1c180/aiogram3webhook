from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def reviews_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Канал с отзывами", url="https://t.me/+uRZQX48FCTc2Yjky")
    kb.button(text="Оставить отзыв", url="https://forms.gle/W6wqLGCowcc5d6SV7")
    kb.button(text="Назад", callback_data="back_to_main")
    kb.adjust(1)
    return kb.as_markup()