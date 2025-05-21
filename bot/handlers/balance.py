from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from bot.database import SessionLocal
from bot.models import User
from bot.keyboards import get_spin_keyboard

router = Router()

@router.callback_query(F.data == "buy_coins")
async def handle_buy_coins(call: CallbackQuery):
    user_id = call.from_user.id

    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            # Новый пользователь — создаём и приветствуем
            user = User(user_id=user_id, score=1000)
            session.add(user)
            await session.commit()

            await call.message.answer(
                "👋 Добро пожаловать в слот-бот 🎰\n\n"
                "Каждая попытка стоит 30 монет. За джекпот можно получить до 300 монет!\n\n"
                "💰 Мы начислили вам 1000 монет на старт. Удачи!",
                reply_markup=get_spin_keyboard()
            )
        else:
            # Существующий пользователь — даём 500 монет
            await session.refresh(user)
            user.score += 500
            await session.commit()

            await call.message.answer(
                "💳 Функционал покупки монет за звёзды скоро появится!\n"
                "А пока держи +500 монет за наш счёт 💰",
                reply_markup=get_spin_keyboard()
            )

    await call.answer()
