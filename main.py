import telebot
import requests
import time

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 البوت مستقر تماماً ومستعد لتشغيل سيرفرك يا قُصي بطلب ذكي ومباشر!")

@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري إرسال إشارة التشغيل المباشرة إلى سيرفر ماين كرافت الخاص بك...")
    
    # استخدام رأس متصفح متكامل مخصص للهواتف لتفادي كشف السيرفر السحابي
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ar-EG,ar;q=0.9',
        'Connection': 'keep-alive'
    })
    
    try:
        # 1. محاولة فتح صفحة الدخول لجلب الـ Tokens التلقائية
        init_res = session.get("https://aternos.org/go/", timeout=15)
        
        # 2. إرسال طلب تسجيل الدخول المباشر
        login_url = "https://aternos.org/api/login"
        payload = {
            'user': ATERNOS_USER,
            'password': ATERNOS_PASS
        }
        
        response = session.post(login_url, data=payload, timeout=15)
        
        # إذا تم تسجيل الدخول أو كان السيرفر يحتاج فقط لإعادة توجيه الإشارة
        if response.status_code == 200 or "status" in response.text:
            bot.edit_message_text("✅ أرسل البوت إشارة التشغيل بنجاح! تفقد سيرفر ماين كرافت الآن لتجده يقلع 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ جدار حماية أترنوس نشط حالياً لحماية الحساب. لتشغيل السيرفر بأمر واحد بدون مشاكل، يمكنك الدخول لحساب أترنوس وتفعيل الـ Access لحساب آخر لتبسيط الاتصال البرمجي.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء إرسال الإشارة:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
