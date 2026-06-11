import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# إعداد السجلات لمراقبة العمليات والأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن التلجرام الخاص بك
TELEGRAM_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# مفتاح جوجل جيميناي الخاص بك مدمج وجاهز
GEMINI_API_KEY = "AQ.Ab8RN6I3OKsk-OwfxKBRtRb7_0Sw44aE8KbvOifpps07_7G0Xg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على أمر البدء"""
    await update.message.reply_text("أهلاً بك! أنا بوت ذكي مدعوم بـ Google Gemini ومستقر 24/7. أرسل لي أي سؤال وسأجيبك فوراً! 🤖🔥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الاتصال المباشر بـ Google Gemini API السريع والمستقر"""
    user_message = update.message.text
    
    # إظهار حالة "جاري الكتابة..." في التلجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # رابط الـ API الرسمي لنموذج جيميناي
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": user_message}]}]
        }
        
        # إرسال الطلب لجوجل
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # استخراج رد الذكاء الاصطناعي
            bot_reply = data['candidates'][0]['content']['parts'][0]['text']
        else:
            logging.error(f"Gemini Error: {response.text}")
            bot_reply = "عذراً، واجهت مشكلة في معالجة الطلب من خوادم جوجل حالياً. حاول مجدداً."
            
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، حدث خطأ داخلي أثناء الاتصال بالذكاء الاصطناعي. حاول مرة أخرى.")

def main():
    """بدء تشغيل البوت"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("⚡ البوت يعمل الآن بنجاح واستقرار على جيميناي...")
    application.run_polling()

if __name__ == '__main__':
    main()
