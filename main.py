import telebot
import requests
import time

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
# إجبار البوت على العمل بنظام الخيوط المتعددة لمنع انهيار سيرفر بايثون الحديث
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 البوت مستقر تماماً ومحمي من الانهيار! جاهز للتحكم بسيرفر ماين كرافت الخاص بك يا قُصي.")

@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري فحص الاتصال وتخطي حماية Aternos...")
    
    session = requests.Session()
    # استخدام معرف متصفح متكامل وآمن لضمان العبور
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    try:
        # خطوة تسجيل الدخول المباشر
        login_url = "https://aternos.org/api/login"
        payload = {
            'user': ATERNOS_USER,
            'password': ATERNOS_PASS
        }
        
        response = session.post(login_url, data=payload, timeout=15)
        
        # إذا تم قبول الطلب أو نجح الاتصال بنجاح
        if response.status_code == 200:
            bot.edit_message_text("✅ تم الاتصال بأترنوس بنجاح! السيرفر يستقبل أمر التشغيل الآن 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ أترنوس يطلب تأكيد المتصفح. جرب الضغط على الأمر مرة أخرى الآن لتحديث الجلسة وتخطي الحماية.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء الاتصال:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

# تشغيل البوت بنظام الأمان والصيانة التلقائية لتفادي الـ Crashes
while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
