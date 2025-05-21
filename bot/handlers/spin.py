from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, CallbackQuery
from asyncio import sleep
import random

from bot.database import SessionLocal
from bot.models import User
from bot.dice_check import get_score_change, get_combo_parts
from bot.keyboards import get_spin_keyboard, get_buy_keyboard
from bot.utils.user import get_or_create_user

router = Router()

LOSE_MESSAGES = [
    "😢 Не повезло, попробуйте ещё!",
    "🎲 Почти! Но не в этот раз.",
    "🙈 Джекпот убежал, но вы его почти поймали!",
    "😬 Увы, пусто... но следующий шанс уже близко!",
    "🫣 Эх, не тот ролл. Попробуйте ещё!"
]

# Унифицированный handler
async def handle_spin(user_id: int, send_func):
    async with SessionLocal() as session:
        user = await get_or_create_user(user_id, session)

        if user.score < 30:
            await send_func("У вас недостаточно монет. Пополните баланс ⭐", reply_markup=get_buy_keyboard())
            return

        user.score -= 30
        user.spins += 1
        await session.commit()

        dice_msg = await send_func("🎰 Крутим слот...", reply_dice=True)
        await sleep(2.0)

        value = dice_msg.dice.value
        score_change = get_score_change(value)

        if score_change > 0:
            user.score += score_change
            user.loss_streak = 0
            result_text = f"🎉 Поздравляем! Вы выиграли {score_change} монет!\n"
            if score_change == 300:
                result_text += "🏆 Это Джекпот! Великолепно!"
        else:
            user.loss_streak += 1
            result_text = random.choice(LOSE_MESSAGES)
            if user.loss_streak >= 5:
                user.score += 10
                result_text += "\n🎁 Бонус: +10 монет за активность!"
                user.loss_streak = 0

        await session.commit()

        combo = " | ".join(get_combo_parts(value))
        await send_func(
            f"🎰 Комбинация: {combo}\n"
            f"{result_text}\n"
            f"💰 Баланс: {user.score} монет",
            reply_markup=get_spin_keyboard()
        )

# Slot emoji
@router.message(lambda m: m.dice and m.dice.emoji == DiceEmoji.SLOT_MACHINE)
async def handle_slot_dice(message: Message):
    await handle_spin(message.from_user.id, lambda text, **kwargs: message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE) if kwargs.get("reply_dice") else message.answer(text, **kwargs))

# Текст "крутить"
@router.message(F.text.lower().contains("крутить"))
async def handle_text(message: Message):
    await handle_spin(message.from_user.id, lambda text, **kwargs: message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE) if kwargs.get("reply_dice") else message.answer(text, **kwargs))

# Кнопка "Крутить ещё"
@router.callback_query(F.data == "spin")
async def handle_button(call: CallbackQuery):
    await handle_spin(call.from_user.id, lambda text, **kwargs: call.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE) if kwargs.get("reply_dice") else call.message.answer(text, **kwargs))
    await call.answer()
