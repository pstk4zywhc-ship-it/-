from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "ضع_التوكن_هنا"

words = {
    "hello": "مرحبا",
    "book": "كتاب",
    "apple": "تفاحة",
    "water": "ماء",
    "computer": "حاسوب",
    "school": "مدرسة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 أهلاً بك في بوت تعلم الإنجليزية!\n\n"
        "أرسل كلمة إنجليزية وسأعطيك معناها بالعربية."
    )

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in words:
        await update.message.reply_text(
            f"✅ {text}\n📖 المعنى: {words[text]}"
        )
    else:
        await update.message.reply_text(
            "❌ لا أعرف هذه الكلمة بعد."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, learn))

print("Bot is running...")
app.run_polling()"

words = {
    "hello": "مرحبا",
    "book": "كتاب",
    "apple": "تفاحة",
    "water": "ماء",
    "computer": "حاسوب",
    "school": "مدرسة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 أهلاً بك في بوت تعلم الإنجليزية!\n\n"
        "أرسل كلمة إنجليزية وسأعطيك معناها بالعربية."
    )

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in words:
        await update.message.reply_text(
            f"✅ {text}\n📖 المعنى: {words[text]}"
        )
    else:
        await update.message.reply_text(
            "❌ لا أعرف هذه الكلمة بعد."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, learn))

print("Bot is running...")
app.run_polling()
