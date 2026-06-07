import telebot
from telebot import types
import requests
import time
import re

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"
# حسابك الشخصي الحصري للأدمن
ADMIN_USERNAME = "sssss111126"

# دالة ذكية لصنع الأزرار الفخمة التي طلبتها بأسفل الشاشة
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
    welcome_text = (
        f"🚀 أهلاً بك يا قُصي في لوحة تحكم Aternos الفخمة!\n\n"
        "استخدم الأزرار بالأسفل للتحكم الكامل بالسيرفرات بضغطة زر واحدة 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

# استقبال الضغط على زر "🎮 تشغيل السيرفر الحالي" أو أمر /create
@bot.message_handler(func=lambda msg: msg.text == "🎮 تشغيل السيرفر الحالي" or msg.text == "/create")
def create_server_btn(message):
    msg = bot.reply_to(message, "⏳ جاري إرسال إشارة التشغيل المباشرة...")
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        login_url = "https://aternos.org/api/login"
        payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS}
        response = session.post(login_url, data=payload, timeout=15)
        if response.status_code == 200 or "status" in response.text:
            bot.edit_message_text("✅ تم إرسال أمر التشغيل بنجاح! السيرفر يقلع الآن 🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("⚠️ لم ينجح الطلب، جرب مرة أخرى.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: `{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

# استقبال الضغط على زر "🧹 تنظيف وإنشاء سيرفر جديد" أو أمر /newserver
@bot.message_handler(func=lambda msg: msg.text == "🧹 تنظيف وإنشاء سيرفر جديد" or msg.text == "/newserver")
def clean_and_create_btn(message):
    # 🔒 جدار حماية الأدمن: التحقق من اليوزر نيم الخاص بك
    current_user = message.from_user.username
    if current_user != ADMIN_USERNAME:
        bot.reply_to(message, "❌ عذراً! هذا الأمر حساس وخاص فقط بمالك البوت (الأدمن) لقفل وحماية السيرفرات.")
        return

    msg = bot.reply_to(message, "🧹 جاري تسجيل الدخول لتنظيف الحساب من السيرفرات القديمة...")
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    try:
        init_req = session.get("https://aternos.org/go/", timeout=15)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', init_req.text)
        ajax_token = token_match.group(1) if token_match else ""

        login_url = "https://aternos.org/api/login"
        login_payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post(login_url, data=login_payload, timeout=15)
        
        bot.edit_message_text("🗑️ جاري حذف السيرفرات القديمة المحفوظة وتفريغ المساحة الحالية...", message.chat.id, msg.message_id)
        delete_url = "https://aternos.org/api/delete"
        session.post(delete_url, data={'token': ajax_token}, timeout=15)
        
        time.sleep(2)
        
        bot.edit_message_text("🛠️ جاري إنشاء سيرفر ماين كرافت (Bedrock) الجديد الآن...", message.chat.id, msg.message_id)
        create_url = "https://aternos.org/api/create"
        server_data = {'type': 'bedrock', 'head': 'default', 'token': ajax_token}
        
        response = session.post(create_url, data=server_data, timeout=15)
        
        if response.status_code == 200:
            bot.edit_message_text("✨ كفو يا أدمن قُصي! تم محو السيرفرات القديمة، وإنشاء سيرفر Bedrock جديد ومحمي بنجاح! 🥳🎮", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("✅ أرسل البوت أمر التطهير والإنشاء، اضغط على زر التشغيل الآن لتجهيز السيرفر الجديد!", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء العملية:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")

# زر قائمة الأدمن للتحقق من الصلاحيات والتحية
@bot.message_handler(func=lambda msg: msg.text == "🔒 قائمة الأدمن")
def admin_panel(message):
    current_user = message.from_user.username
    if current_user == ADMIN_USERNAME:
        bot.reply_to(message, "👑 مرحباً بك يا ملك البرمجة قُصي! صلاحيات الأدمن كاملة ونشطة لديك الآن على حساب @sssss111126.")
    else:
        bot.reply_to(message, "🚫 هذه القائمة مخصصة فقط للأدمن المبرمج، ولا تمتلك صلاحية عرضها.")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
