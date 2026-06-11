import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import g4f

# إعداد السجلات لمراقبة العمليات والأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# التوكن الخاص بك مدمج وجاهز للعمل
TELEGRAM_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر البدء"""
    await update.message.reply_text("أهلاً بك! أنا بوت ذكي مثل ChatGPT. أرسل لي أي سؤال وسأجيبك فوراً! 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال رسالة المستخدم للذكاء الاصطناعي والرد بها"""
    user_message = update.message.text
    
    # إظهار أن البوت يكتب الآن (typing...)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # طلب الإجابة من الذكاء الاصطناعي مجاناً
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o,
            messages=[{"role": "user", "content": user_message}],
        )
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في معالجة طلبك حالياً. حاول مرة أخرى.")

def main():
    """بدء تشغيل البوت"""
    # تشغيل الاتصال بالتلجرام باستخدام التوكن المدمج
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("⚡ البوت يعمل الآن بنجاح واستقرار...")
    application.run_polling()

if __name__ == '__main__':
    main()
