import sqlite3
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7914434174"
ADMIN_ID = 8064307351:AAG7KtS81OJ4GxlszjRxDmwwhRto7Yyb9-M

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT
)
""")
conn.commit()

def main_menu():
    keyboard = [
        ["📄 درباره ما", "📞 تماس با ما"],
        ["👤 پروفایل"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update, context):
    user = update.effective_user
    cursor.execute("INSERT OR IGNORE INTO users (id, first_name) VALUES (?, ?)", (user.id, user.first_name))
    conn.commit()

    await update.message.reply_text(
        f"سلام {user.first_name} 👋",
        reply_markup=main_menu()
    )

async def handle_message(update, context):
    text = update.message.text
    user = update.effective_user

    if text == "📄 درباره ما":
        await update.message.reply_text("این یک ربات شخصی سازی شده است.")
    
    elif text == "📞 تماس با ما":
        await update.message.reply_text("تماس: example@gmail.com")

    elif text == "👤 پروفایل":
        await update.message.reply_text(f"نام: {user.first_name}\nآیدی: {user.id}")

async def admin(update, context):
    if update.effective_user.id == ADMIN_ID:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        await update.message.reply_text(f"👑 پنل ادمین\nتعداد کاربران: {count}")
    else:
        await update.message.reply_text("دسترسی ندارید ❌")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
