import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# إعداد السجلات لمراقبة العمليات والأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن التلجرام الخاص بك
TELEGRAM_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# مفتاح جوجل جيميناي الحقيقي (احرص على استخراج المفتاح الصحيح تباعاً للخطوات بالأسفل)
GEMINI_API_KEY = "ضع_مفتاح_جيميناي_الحقيقي_هنا"

# إعداد عميل جيميناي الرسمي
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY != "ضع_مفتاح_جيميناي_الحقيقي_هنا" else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر البدء"""
    await update.message.reply_text("أهلاً بك! أنا بوت ذكي مدعوم بـ Google Gemini ومستقر 24/7. أرسل لي أي سؤال وسأجيبك فوراً! 🤖🔥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الاتصال عبر مكتبة جوجل الرسمية وبشكل متوافق مع الحزم الحديثة"""
    user_message = update.message.text
    
    # إظهار حالة "جاري الكتابة..." في التلجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    if not client:
        await update.message.reply_text("⚠️ يرجى إضافة مفتاح GEMINI_API_KEY الحقيقي داخل الكود أولاً!")
        return

    try:
        # تشغيل طلب توليد النص في خيط منفصل لمنع تجميد البوت
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
        await update.message.reply_text("عذراً، واجهت مشكلة في معالجة الطلب من خوادم جوجل. تأكد من صحة الـ API Key وحاول مجدداً.")

def main():
    """بدء تشغيل البوت"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("⚡ البوت يعمل الآن بنجاح واستقرار...")
    application.run_polling()

if __name__ == '__main__':
    main()
