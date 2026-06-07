import telebot
from aternosapi import AternosAPI

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# بيانات الحساب المضافة بنجاح 👍
ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أهلاً بك يا قُصي! البوت متصل الآن بجهاز Railway وجاهز للتحكم بـ Aternos!")

@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري محاولة الاتصال بـ Aternos وبدء تشغيل السيرفر...")
    
    try:
        # الاتصال المباشر بالحساب
        aternos = AternosAPI(ATERNOS_USER, ATERNOS_PASS)
        servers = aternos.get_servers()
        
        if servers:
            server = servers[0]
            server.start()
            bot.edit_message_text("✅ تم تشغيل سيرفر ماين كرافت بنجاح! استمتع باللعب يا بطل 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ لم يتم العثور على أي سيرفرات داخل هذا الحساب.", message.chat.id, msg.message_id)
            
    except Exception as e:
        error_msg = str(e)
        if "Cloudflare" in error_msg or "Forbidden" in error_msg:
            bot.edit_message_text("⚠️ أترنوس يطلب تأكيد المتصفح. لتشغيل السيرفر فوراً بدون قيود، يرجى تفعيل خيار الـ Share في حسابك لأي حساب آخر.", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text(f"❌ حدث خطأ أثناء الاتصال:\n`{error_msg}`", message.chat.id, msg.message_id, parse_mode="Markdown")

bot.infinity_polling()
