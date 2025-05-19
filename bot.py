
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3, random

# Инициализация базы данных
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 1000,
    spins INTEGER DEFAULT 0,
    loss_streak INTEGER DEFAULT 0
)
""")
conn.commit()

# Регистрация пользователя
def register_user(user_id):
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id) VALUES (?)
    """, (user_id,))
    conn.commit()

# Получение информации о пользователе
def get_user_data(user_id):
    cursor.execute("SELECT coins, spins, loss_streak FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

# Обновление информации
def update_user_data(user_id, coins, spins, loss_streak):
    cursor.execute("""
        UPDATE users SET coins = ?, spins = ?, loss_streak = ? WHERE user_id = ?
    """, (coins, spins, loss_streak, user_id))
    conn.commit()

# Главное меню
def main_menu(spin_cost):
    buttons = [
        [InlineKeyboardButton(f"🎰 Крутить джекпот ({spin_cost} монет)", callback_data="spin")],
        [InlineKeyboardButton("💵 Купить монеты за звезды", callback_data="buy")]
    ]
    return InlineKeyboardMarkup(buttons)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    register_user(user_id)
    coins, spins, _ = get_user_data(user_id)
    spin_cost = 30 + (spins // 10) * 10
    await update.message.reply_text(
        f"Добро пожаловать в Джекпот Бот! 💰\nУ вас {coins} монет.\n"
        f"Стоимость прокрутки: {spin_cost} монет.",
        reply_markup=main_menu(spin_cost)
    )

# Обработка кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    register_user(user_id)
    coins, spins, loss_streak = get_user_data(user_id)
    spin_cost = 30 + (spins // 10) * 10

    if query.data == "spin":
        await query.message.reply_text("🎰")  # Добавлено отображение слота

        if coins < spin_cost:
            await query.answer()
            await query.edit_message_text(
                "Недостаточно монет! Попробуйте купить их за звезды.",
                reply_markup=main_menu(spin_cost)
            )
        else:
            coins -= spin_cost
            spins += 1

            is_jackpot = random.random() < 0.05  # 5% шанс
            if is_jackpot:
                coins += 300
                result = "🎉 Джекпот!"
                loss_streak = 0
            else:
                result = random.choice(["💀 Не повезло", "🍀 Почти!"])
                loss_streak += 1

                if loss_streak >= 5:
                    coins += 10
                    result += "\n🔥 Бонус за серию проигрышей: +10 монет!"
                    loss_streak = 0

            update_user_data(user_id, coins, spins, loss_streak)
            spin_cost = 30 + (spins // 10) * 10

            await query.answer()
            await query.edit_message_text(
                f"{result}\nВаш баланс: {coins} монет.\nСтоимость следующей прокрутки: {spin_cost} монет.",
                reply_markup=main_menu(spin_cost)
            )

    elif query.data == "buy":
        await query.answer()
        await query.edit_message_text(
            "🔔 Покупка за Telegram-звезды пока в разработке.\nОжидайте поддержку Telegram Stars.",
            reply_markup=main_menu(spin_cost)
        )

# Запуск приложения
app = ApplicationBuilder().token("ВАШ_ТОКЕН_ОТ_BOTFATHER").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.run_polling()
