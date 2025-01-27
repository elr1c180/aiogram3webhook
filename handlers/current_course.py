from aiogram import Router, types, F

from asgiref.sync import sync_to_async
from config import BASE_DIR
import django
import os, sys
from core.models import Themes

from kb.current_course_btn import course_btn

sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chim_admin.settings')
django.setup()

router = Router()

@sync_to_async
def get_course_by_id(course_id: int):
    try:
        return Themes.objects.get(id=course_id)
    except Themes.DoesNotExist:
        return None

@router.callback_query(lambda c: c.data.startswith('course_'))
async def reviews_router(callback: types.CallbackQuery):
    await callback.message.delete()

    # Получаем информацию о курсе
    course_id = int(callback.data.split('_')[1])
    current_course = await get_course_by_id(course_id)
    kb = await course_btn(course_id)
    if current_course:
        # Ответ с деталями курса
        await callback.message.answer(
            f"Вы выбрали <b>{current_course.name}</b>\n\n<b>Описание:</b> {current_course.description}\n\n<b>Цена:</b> {current_course.price} Рублей\n\nНажимая кнопку 'Купить' вы соглашаетесь с <a href='https://drive.google.com/file/d/1oQluYUhUNeDcdjfFWLwhkNSS40rIPDxs/view?usp=sharing' >договором оферты</a>",
            reply_markup=kb,
            parse_mode='html'
        )
    else:
        await callback.message.answer("Курс не найден.")