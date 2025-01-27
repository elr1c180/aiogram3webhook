from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BASE_DIR
import django
import os, sys
from core.models import Themes

sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chim_admin.settings')
django.setup()

from asgiref.sync import sync_to_async


@sync_to_async
def get_course_by_id(course_id: int):
    try:
        return Themes.objects.get(id=course_id)
    except Themes.DoesNotExist:
        return None

async def course_btn(id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    theme = await get_course_by_id(id)
    

    kb.button(text="Купить", callback_data=f"buy_{theme.id}")

    kb.button(text="Назад", callback_data="buy_course")
    kb.adjust(1)
    
    return kb.as_markup()
