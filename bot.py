from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import subprocess

TOKEN = "YOUR_BOT_TOKEN"

server_process = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 تشغيل السيرفر", callback_data="start_server")],
        [InlineKeyboardButton("⛔ إيقاف السيرفر", callback_data="stop_server")],
        [InlineKeyboardButton("📊 حالة السيرفر", callback_data="status_server")],
    ]

    await update.message.reply_text(
        "🎮 لوحة التحكم بسيرفر ماين كرافت",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global server_process

    query = update.callback_query
    await query.answer()

    if query.data == "start_server":
        if server_process is None:
            server_process = subprocess.Popen(
                ["java", "-Xmx2G", "-Xms2G", "-jar", "server.jar", "nogui"]
            )
            await query.edit_message_text("✅ تم تشغيل السيرفر")
        else:
            await query.edit_message_text("⚠️ السيرفر شغال بالفعل")

    elif query.data == "stop_server":
        if server_process:
            server_process.terminate()
            server_process = None
            await query.edit_message_text("🛑 تم إيقاف السيرفر")
        else:
            await query.edit_message_text("❌ لا يوجد سيرفر شغال")

    elif query.data == "status_server":
        if server_process:
            await query.edit_message_text("🟢 السيرفر يعمل")
        else:
            await query.edit_message_text("🔴 السيرفر متوقف")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
