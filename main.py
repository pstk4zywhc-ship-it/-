import telebot
from python_aternos import Client

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# بيانات حسابك الحالي مباشرة
ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أهلاً بك يا قُصي! البوت مستقر الآن على سيرفر Railway وجاهز للتحكم بـ Aternos بنفس حسابك!")

@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري الاتصال بحسابك في Aternos وتوصيل السيرفر...")
    
    try:
        # تسجيل الدخول بنظام المحاكاة الحديث لتخطي الحماية
        aternos = Client.from_credentials(ATERNOS_USER, ATERNOS_PASS)
        servers = aternos.list_servers()
        
        if servers:
            myserver = servers[0]
            # أمر تشغيل السيرفر مباشرة
            myserver.start()
            bot.edit_message_text("✅ أبشرك يا قُصي! تم تشغيل سيرفر ماين كرافت بنجاح وطار الحظر! ادخل العب الآن 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ لم يتم العثور على أي سيرفرات داخل هذا الحساب.", message.chat.id, msg.message_id)
            
    except Exception as e:
        error_msg = str(e)
        bot.edit_message_text(f"❌ حدث خطأ أثناء محاولة التشغيل:\n`{error_msg}`", message.chat.id, msg.message_id, parse_mode="Markdown")

bot.infinity_polling()
