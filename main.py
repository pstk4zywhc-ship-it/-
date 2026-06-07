import telebot

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أهلاً بك يا قُصي! البوت شغال الآن بأعلى سرعة على سيرفر Railway بدون أي تقطيع!")

@bot.message_handler(commands=['create'])
def create(message):
    bot.reply_to(message, "⚙️ ميزة الاتصال بـ Aternos جاري تجهيزها بنظام حماية متطور لمنع الحظر.")

bot.infinity_polling()
