from aiogram import Router, types, F
from aiogram.filters import Command
from kb.courses import courses_btns

from config import BASE_DIR
import django
import os, sys
from core.models import Themes

sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chim_admin.settings')
django.setup()

router = Router()

@router.callback_query(F.data == 'buy_course')
async def buy_courses_btn(callback: types.CallbackQuery):
    await callback.message.delete()

    kb = await courses_btns()

    await callback.message.answer(
        "Список доступных курсов:",
        reply_markup=kb,
        parse_mode='html'
        )