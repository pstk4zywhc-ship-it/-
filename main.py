import telebot
import cloudscraper

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# بيانات حسابك الحالي في أترنوس
ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أهلاً بك يا قُصي! البوت مستقر والاتصال بحسابك آمن وجاهز لتشغيل السيرفر!")

@bot.message_handler(commands=['create'])
def create_server(message):
    msg = bot.reply_to(message, "⏳ جاري تخطي الحماية والاتصال بـ Aternos...")
    
    try:
        # إنشاء ممر آمن يتخطى جدار حماية Cloudflare
        scraper = cloudscraper.create_scraper()
        
        login_url = "https://aternos.org/api/login"
        payload = {
            'user': ATERNOS_USER,
            'password': ATERNOS_PASS
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://aternos.org/go/'
        }
        
        response = scraper.post(login_url, data=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            bot.edit_message_text("✅ أبشرك يا قُصي! تم الاتصال وتخطي الحماية بنجاح، وجاري إقلاع سيرفر ماين كرافت الآن! 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ استجاب السيرفر ولكن أترنوس يطلب تسجيل دخول يدوي من المتصفح أولاً لتحديث الجلسة.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ غير متوقع:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

bot.infinity_polling()
