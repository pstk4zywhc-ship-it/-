import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات لمراقبة العمليات والأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# التوكن الخاص بك
TELEGRAM_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر البدء"""
    await update.message.reply_text("أهلاً بك! أنا بوت ذكي مثل ChatGPT يعمل الآن بشكل مستقر 24/7. أرسل لي أي سؤال! 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الاتصال المباشر بالذكاء الاصطناعي بدون مكتبات خارجية وسيطة"""
    user_message = update.message.text
    
    # إظهار حالة "جاري الكتابة..." في التلجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # رابط مباشر لـ API ذكاء اصطناعي مجاني ومستقر
        api_url = f"https://dev-gpts.pantheonsite.io/wp-admin/js/api.php?text={user_message}"
        
        # إرسال الطلب وجلب الرد
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            bot_reply = response.text.strip()
            # إذا كان الرد فارغاً نضع رسالة بديلة
            if not bot_reply:
                bot_reply = "لم أستطع معالجة النص، يرجى المحاولة مرة أخرى."
        else:
            bot_reply = "عذراً، الخادم مشغول حالياً. حاول مجدداً."
            
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في الاتصال بالذكاء الاصطناعي حالياً. حاول مرة أخرى.")

def main():
    """بدء تشغيل البوت"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("⚡ البوت يعمل الآن بنجاح واستقرار...")
    application.run_polling()

if __name__ == '__main__':
    main()
