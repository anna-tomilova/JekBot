from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database import SessionLocal, User
from bot.keyboards import get_spin_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            # Новый пользователь
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()
            await message.answer(
                "👋 Добро пожаловать в Джекпот Бот!\n"
                "Правила просты:\n"
                "🎰 Крути слот-машину за 30 монет\n"
                "🏆 Выиграй до 300 монет за один спин!\n\n"
                f"💰 Ваш баланс: {user.score} монет",
                reply_markup=get_spin_keyboard()
            )
        else:
            # Повторный вход
            await message.answer(
                f"💰 Ваш текущий баланс: {user.score} монет",
                reply_markup=get_spin_keyboard()
            )
