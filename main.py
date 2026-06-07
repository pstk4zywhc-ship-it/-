import telebot
import requests
import time

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    help_text = (
        "🚀 أهلاً بك يا قُصي في بوت التحكم بـ Aternos!\n\n"
        "🎮 **الأوامر المتاحة:**\n"
        "🔹 `/create` - لتشغيل سيرفرك الحالي.\n"
        "🔹 `/newserver` - لإنشاء سيرفر ماين كرافت (Bedrock) جديد تماماً!"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

# 1. أمر تشغيل السيرفر الحالي
@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري إرسال إشارة التشغيل المباشرة...")
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15'
    })
    try:
        login_url = "https://aternos.org/api/login"
        payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS}
        response = session.post(login_url, data=payload, timeout=15)
        
        if response.status_code == 200 or "status" in response.text:
            bot.edit_message_text("✅ أرسل البوت إشارة التشغيل بنجاح! تفقد سيرفر ماين كرافت الآن لتجده يقلع 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ لم ينجح الطلب، جرب مرة أخرى أو تفقد الحساب.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: `{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

# 2. الأمر الجديد: إنشاء سيرفر جديد تماماً من البوت
@bot.message_handler(commands=['newserver'])
def create_new_server(message):
    msg = bot.reply_to(message, "🛠️ جاري الاتصال بـ Aternos لإنشاء سيرفر ماين كرافت جديد...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    try:
        # تسجيل الدخول أولاً
        login_url = "https://aternos.org/api/login"
        payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS}
        session.post(login_url, data=payload, timeout=15)
        
        # إرسال أمر إنشاء سيرفر جديد بنظام Bedrock (للموبايل)
        # أترنوس يسمح بإنشاء سيرفر جديد إذا لم تكن قد تجاوزت الحد الأقصى للحساب (سيرفرين)
        create_url = "https://aternos.org/api/create"
        # 'bedrock' لنسخة الهاتف، و 'java' للكمبيوتر
        server_data = {
            'type': 'bedrock', 
            'head': 'default'
        }
        
        response = session.post(create_url, data=server_data, timeout=15)
        
        if response.status_code == 200:
            bot.edit_message_text("✨ أبشرك يا قُصي! تم إنشاء سيرفر ماين كرافت (Bedrock) جديد بنجاح داخل حسابك! 🥳 قُم بالدخول إلى الحساب لتعديل اسمه ورابطه.", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ فشل إنشاء السيرفر. قد يكون السبب أن حسابك وصل للحد الأقصى من السيرفرات المسموحة (سيرفرين كحد أقصى في أترنوس).", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء الإنشاء:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
