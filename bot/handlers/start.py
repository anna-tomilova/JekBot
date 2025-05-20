from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select
from bot.database import SessionLocal
from bot.models import User
from bot.keyboards import get_spin_keyboard

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    user_id = message.from_user.id

    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(user_id=user_id, score=1000)
            session.add(user)
            await session.commit()
            text = (
                "👋 Добро пожаловать в слот-бота!\n\n"
                "🔹 У вас есть 1000 монет.\n"
                "🔹 Каждое вращение стоит 30 монет.\n"
                "🔹 Вы можете выиграть до 300 монет за раз!\n\n"
                "Начнем?"
            )
        else:
            text = f"💰 Ваш текущий баланс: {user.score} монет"

    await message.answer(text, reply_markup=get_spin_keyboard())
