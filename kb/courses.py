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

async def courses_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    themes = await sync_to_async(list)(Themes.objects.all())
    
    for theme in themes:
        kb.button(text=theme.name, callback_data=f"course_{theme.id}")
    
    kb.button(text="Назад", callback_data="back_to_main")
    kb.adjust(1)
    
    return kb.as_markup()

