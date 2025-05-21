from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_spin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Крутить ещё", callback_data="spin")],
        [InlineKeyboardButton(text="⭐ Купить монеты", callback_data="buy_coins")]
    ])

def get_buy_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Купить монеты", callback_data="buy_coins")]
        ]
    )
