from aiogram import Router, types, F
from aiogram.filters import Command
from kb.start_kb import start_bot
import re

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"<b>Приветствую, {message.from_user.first_name}!</b>",
        reply_markup=start_bot(),
        parse_mode='html'
        )

    # user_status = await message.bot.get_chat_member(chat_id="-4648273731", user_id=message.chat.id)
    # print(dict(user_status)['status'])

@router.callback_query(F.data == 'back_to_main')
async def start_msg(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
         f"<b>Приветствую, {callback.from_user.first_name}!</b>",
        reply_markup=start_bot(),
        parse_mode='html'
    )
    