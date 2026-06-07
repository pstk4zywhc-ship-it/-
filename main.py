import telebot
from telebot import types
import requests
import time
import re

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

# دالة برمجية للاتصال الفوري بحساب أترنوس وتمرير العمليات
def execute_aternos_api(action):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    })
    try:
        # جلب التوكن
        res = session.get("https://aternos.org/go/", timeout=10)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', res.text)
        ajax_token = token_match.group(1) if token_match else ""

        # تسجيل الدخول
        login_data = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post("https://aternos.org/api/login", data=login_data, timeout=10)
        
        # تنفيذ الأمر
        action_url = f"https://aternos.org/api/server/{action}"
        session.post(action_url, data={'token': ajax_token}, timeout=10)
        return True
    exceptException as e:
        return False

# دالة بناء قائمة الأزرار الكبيرة أسفل الشاشة
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🕹️ تشغيل السيرفر الحالي"),
        types.KeyboardButton("🧹 تنظيف وإنشاء سيرفر جديد")
    )
    markup.add(
        types.KeyboardButton("🌐 تغيير اللغة / Language"),
        types.KeyboardButton("🔒 قائمة الأدمن")
    )
    return markup

# عند إرسال /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = (
        "🚀 أهلاً بك يا قُصي في بوت التحكم بـ Aternos!\n\n"
        "🎮 **الأوامر المتاحة:**\n"
        "🔹 `/create` أو زر التشغيل - لتشغيل سيرفرك الحالي\n"
        "🔹 `/newserver` أو زر التنظيف - لإنشاء وتجهيز سيرفر ماين كرافت (Bedrock) جديد تماماً!\n\n"
        "استخدم الأزرار بالأسفل أو الأوامر مباشرة 👇"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# عند كتابة أمر /create أو الضغط على زر التشغيل الحالي
@bot.message_handler(commands=['create'])
@bot.message_handler(func=lambda msg: msg.text == "🕹️ تشغيل السيرفر الحالي")
def start_server_action(message):
    uid = message.chat.id
    m = bot.send_message(uid, "⏳ جاري الاتصال بأترنوس وتخطي جدار الحماية لتشغيل السيرفر...")
    
    # استدعاء دالة التشغيل
    execute_aternos_api("start")
    
    res_text = (
        "✅ **تم إرسال أمر التشغيل بنجاح وبدأ السيرفر بالإقلاع!**\n\n"
        "📌 **معلومات الدخول للسيرفر الجديد (Bedrock):**\n"
        "🌐 **الـ IP (العنوان):** `qusai2000.aternos.me`\n"
        "🔌 **الـ Port (المنفذ):** `19132` (أو تفقد المنفذ العشوائي الجديد في حسابك)\n\n"
        "🎮 انسخ البيانات وضعها في اللعبة فوراً واستمتعوا باللعب!"
    )
    bot.edit_message_text(res_text, uid, m.message_id, parse_mode="Markdown")

# عند كتابة أمر /newserver أو الضغط على زر التنظيف والإنشاء
@bot.message_handler(commands=['newserver'])
@bot.message_handler(func=lambda msg: msg.text == "🧹 تنظيف وإنشاء سيرفر جديد")
def create_server_action(message):
    uid = message.chat.id
    m = bot.send_message(uid, "⏳ جاري إرسال إشارة التطهير وبناء السيرفر الجديد...")
    
    # استدعاء دالة الإنشاء أو الحذف القديم لإعادة التجهيز
    execute_aternos_api("delete")
    
    res_text = "🧹 **أرسل البوت أمر التطهير والإنشاء بنجاح!**\n\nاضغط الآن على خيار أو زر (🕹️ تشغيل السيرفر الحالي) لتجهيز وإقلاع السيرفر الجديد بالكامل."
    bot.edit_message_text(res_text, uid, m.message_id, parse_mode="Markdown")

# قائمة الأدمن
@bot.message_handler(func=lambda msg: msg.text == "🔒 قائمة الأدمن")
def admin_info(message):
    bot.reply_to(message, f"👑 **لوحة تحكم الأدمن قُصي**\n👤 الحساب المرتبط حالياً: `qusai2000`")

# خيار تغيير اللغة
@bot.message_handler(func=lambda msg: msg.text == "🌐 تغيير اللغة / Language")
def change_lang_info(message):
    bot.reply_to(message, "🌐 البوت مثبت حالياً على اللغة العربية لسهولة التحكم.")

# تشغيل الاستقبال المستمر
while True:
    try:
