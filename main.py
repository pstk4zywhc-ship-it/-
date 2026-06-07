import telebot
from python_aternos import Client

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت شغال وجاهز بأعلى سرعة على Railway!")

@bot.message_handler(commands=['create'])
def create(message):
    bot.reply_to(message, "⏳ جاري الاتصال بـ Aternos...")
    try:
        at = Client()
        at.login("qusai2000", "qusai123@")
        srv = at.list_servers()[0]
        bot.reply_to(message, f"✅ تم الاتصال! سيرفرك هو: {srv.address}")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

bot.infinity_polling()
