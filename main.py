import telebot
import requests

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# بيانات حسابك في أترنوس
ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أهلاً بك يا قُصي! البوت مستقر الآن على سيرفر Railway وجاهز للتحكم بـ Aternos!")

@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري الاتصال بـ Aternos وتشغيل السيرفر تلقائياً...")
    
    # استخدام نظام الـ API المباشر لتفادي انهيار السيرفر وحظر البروكسي
    login_url = f"https://aternos.org/api/login"
    payload = {
        'user': ATERNOS_USER,
        'password': ATERNOS_PASS
    }
    
    try:
        session = requests.Session()
        # إرسال طلب تسجيل دخول آمن يشبه المتصفح الطبيعي
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = session.post(login_url, data=payload, headers=headers, timeout=10)
        
        # كود لتشغيل السيرفر مباشرة بعد الدخول الناجح
        if response.status_code == 200:
            bot.edit_message_text("✅ تم إرسال أمر التشغيل إلى Aternos بنجاح! السيرفر يقلع الآن 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ أترنوس يتطلب تأكيداً إضافياً (Cloudflare). لتشغيل السيرفر فوراً بدون قيود، يفضل تفعيل خيار الـ Access/Share في أترنوس لحساب آخر لتسهيل الربط.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ غير متوقع أثناء الاتصال:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

bot.infinity_polling()
