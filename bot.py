import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# إعداد السجلات لمراقبة العمليات والأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن التلجرام الخاص بك المدمج
TELEGRAM_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# مفتاح جوجل جيميناي الحقيقي الخاص بك تم دمجه بنجاح هنا
GEMINI_API_KEY = "AQ.Ab8RN6IL0MdnRr2PaqKISoIBMjWqKJMvegcQ74F_J7sk3raQZQ"

# إعداد عميل جيميناي الرسمي باستخدام المفتاح
client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر البدء"""
    await update.message.reply_text("أهلاً بك! أنا بوت ذكي مدعوم بـ Google Gemini ومستقر 24/7. أرسل لي أي سؤال وسأجيبك فوراً! 🤖🔥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الاتصال عبر مكتبة جوجل الرسمية وبشكل متوافق مع الحزم الحديثة"""
    user_message = update.message.text
    
    # إظهار حالة "جاري الكتابة..." في التلجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # تشغيل طلب توليد النص في خلفية آمنة لمنع تجميد البوت
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
            )
        )
        
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logging.error(f"Gemini Library Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في معالجة الطلب من خوادم جوجل. يرجى المحاولة مرة أخرى.")

def main():
    """بدء تشغيل البوت"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("⚡ البوت يعمل الآن بنجاح واستقرار...")
    application.run_polling()

if __name__ == '__main__':
    main()
