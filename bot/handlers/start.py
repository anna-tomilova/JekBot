from aiogram import Router
from aiogram.types import Message
from bot.database import SessionLocal
from bot.utils.user import get_or_create_user
from bot.keyboards import get_spin_keyboard

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    user_id = message.from_user.id
    async with SessionLocal() as session:
        user = await get_or_create_user(user_id, session)

        if user.spins == 0:
            text = (
                "🎉 Добро пожаловать в JekBot\n"
                "Каждый спин стоит 30 монет. Если выпадет удачная комбинация — вы получите монеты обратно с прибылью до 300 монет!\n\n"
                f"💰 Ваш баланс: {user.score} монет\n"
                "Выберите действие:"
            )
        else:

            text = f"💰 Ваш текущий баланс: {user.score} монет"

        await message.answer(text, reply_markup=get_spin_keyboard())