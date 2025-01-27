from aiogram import Router, types, F
from aiogram.filters import Command
from kb.reviews_kb import reviews_btns


router = Router()

@router.callback_query(F.data == 'reviews')
async def reviews_router(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Вы можете <b>ознакомиться</b> или <b>оставить</b> отзыв о нас и нашей работе!",
        reply_markup=reviews_btns(),
        parse_mode='html'
        )