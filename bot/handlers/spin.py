from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, CallbackQuery
from asyncio import sleep
from sqlalchemy import select
from bot.database import SessionLocal
from bot.models import User
from bot.dice_check import get_score_change, get_combo_parts
from bot.keyboards import get_spin_keyboard

router = Router()

@router.message(F.text.lower().contains("крутить"))
async def handle_spin_text(message: Message):
    await handle_spin(message)

@router.callback_query(F.data == "spin")
async def handle_spin_button(call: CallbackQuery):
    await handle_spin(call.message)
    await call.answer()

async def handle_spin(message: Message):
    user_id = message.from_user.id
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()

        if user.score < 30:
            await message.answer("У вас недостаточно монет. Пополните баланс ⭐")
            return

        user.score -= 30
        user.spins += 1
        await session.commit()

        dice_msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
        await sleep(2.0)

        value = dice_msg.dice.value
        score_change = get_score_change(value)

        if score_change > 0:
            user.score += score_change
            user.loss_streak = 0
            result_text = f"🎉 Поздравляем! Вы выиграли {score_change} монет!"
        else:
            user.loss_streak += 1
            result_text = "😢 Не повезло, попробуйте ещё!"
            if user.loss_streak >= 5:
                user.score += 10
                result_text += " Бонус: +10 монет за серию неудач 🎁"
                user.loss_streak = 0

        await session.commit()

        combo = " | ".join(get_combo_parts(value))
        await message.answer(
            f"🎰 Комбинация: {combo}

{result_text}
💰 Баланс: {user.score} монет",
            reply_markup=get_spin_keyboard()
        )
