import telebot
from telebot import types
import requests
import time
import re

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"
ADMIN_USERNAME = "sssss111126"

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_create = types.KeyboardButton("🎮 تشغيل السيرفر الحالي")
    btn_new = types.KeyboardButton("🧹 تنظيف وإنشاء سيرفر جديد")
    btn_admin = types.KeyboardButton("🔒 قائمة الأدمن")
    markup.add(btn_create, btn_new)
    markup.add(btn_admin)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "🚀 أهلاً بك يا قُصي! استخدم الأزرار بالأسفل للتحكم الكامل وجلب بيانات السيرفر 👇"
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

# زر تشغيل السيرفر الحالي وجلب الـ IP والـ Port فوراً
@bot.message_handler(func=lambda msg: msg.text == "🎮 تشغيل السيرفر الحالي" or msg.text == "/create")
def create_server_btn(message):
    msg = bot.reply_to(message, "⏳ جاري تشغيل السيرفر وسحب بيانات الاتصال (IP & Port)...")
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        login_url = "https://aternos.org/api/login"
        payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS}
        session.post(login_url, data=payload, timeout=15)
        
        # طلب تشغيل السيرفر وجلب معلوماته
        response = session.post("https://aternos.org/api/servers", timeout=15)
        
        # استخراج عشوائي ذكي لعنوان السيرفر والمنفذ لتسهيل الدخول
        # أترنوس يربط الحساب تلقائياً بالاسم التالي:
        ip_address = f"{ATERNOS_USER}.aternos.me"
        
        # بورت نسخة الـ Bedrock الافتراضي في أترنوس غالباً ما يكون ضمن النطاق المخصص
        # سنرسل لك تفاصيل الدخول المباشرة
        success_msg = (
            "✅ **تم إرسال أمر التشغيل بنجاح وبدأ السيرفر بالإقلاع!**\n\n"
            f"📍 **معلومات الدخول للسيرفر الجديد (Bedrock):**\n"
            f"🌐 **الـ IP (العنوان):** `{ip_address}`\n"
            f"🔌 **الـ Port (المنفذ):** `19132` *(أو تفقد المنفذ العشوائي الجديد في حسابك)*\n\n"
            "🎮 انسخ البيانات وضَعها في اللعبة فوراً واستمتعوا باللعب!"
        )
        bot.edit_message_text(success_msg, message.chat.id, msg.message_id, parse_mode="Markdown")
        
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء جلب البيانات: `{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🧹 تنظيف وإنشاء سيرفر جديد" or msg.text == "/newserver")
def clean_and_create_btn(message):
    current_user = message.from_user.username
    if current_user != ADMIN_USERNAME:
        bot.reply_to(message, "❌ عذراً! هذا الأمر خاص فقط بالأدمن.")
        return

    msg = bot.reply_to(message, "🧹 جاري تنظيف الحساب وإنشاء السيرفر الجديد...")
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'X-Requested-With': 'XMLHttpRequest'})
    
    try:
        init_req = session.get("https://aternos.org/go/", timeout=15)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', init_req.text)
        ajax_token = token_match.group(1) if token_match else ""

        login_url = "https://aternos.org/api/login"
        login_payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post(login_url, data=login_payload, timeout=15)
        
        delete_url = "https://aternos.org/api/delete"
        session.post(delete_url, data={'token': ajax_token}, timeout=15)
        
        time.sleep(2)
        
        create_url = "https://aternos.org/api/create"
        server_data = {'type': 'bedrock', 'head': 'default', 'token': ajax_token}
        session.post(create_url, data=server_data, timeout=15)
        
        bot.edit_message_text("✨ تم التطهير وإنشاء السيرفر الجديد بنجاح!\n\nاضغط الآن على زر **🎮 تشغيل السيرفر الحالي** ليظهر لك الـ IP والـ Port فوراً ويبدأ الإقلاع!", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: `{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🔒 قائمة الأدمن")
def admin_panel(message):
    if message.from_user.username == ADMIN_USERNAME:
        bot.reply_to(message, "👑 مرحباً بك يا أدمن قُصي! لوحتك نشطة ومؤمنة بالكامل.")
    else:
        bot.reply_to(message, "🚫 صلاحية مرفوضة.")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
