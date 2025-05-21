from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.database import SessionLocal
from bot.utils.user import get_or_create_user  # ⬅️ вот импорт
from bot.keyboards import get_spin_keyboard

router = Router()

@router.callback_query(F.data == "buy_coins")
async def buy_coins(call: CallbackQuery):
    user_id = call.from_user.id
    async with SessionLocal() as session:
        user = await get_or_create_user(user_id, session)

        user.score += 500
        await session.commit()

    await call.message.answer(
        "💳 Функционал покупки монет за звёзды в разработке, а пока держи +500 монет за наш счёт!",
        reply_markup=get_spin_keyboard()
    )
    await call.answer()
