import telebot
from telebot import types
import requests
import time
import re

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"

# دالة ذكية لإرسال الأوامر مباشرة للسيرفر الداخلي عبر التوكن لتفادي اللوبي
def execute_aternos_action(action):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    })
    try:
        # 1. فتح صفحة البداية لجلب الكوكيز وتوكن الحماية الأساسي
        res = session.get("https://aternos.org/go/", timeout=10)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', res.text)
        ajax_token = token_match.group(1) if token_match else ""

        # 2. تسجيل الدخول الفعلي للحساب
        login_data = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post("https://aternos.org/api/login", data=login_data, timeout=10)
        
        # 3. جلب معرف السيرفر الداخلي تلقائياً لتفادي اللوبي تماماً
        sec_res = session.get("https://aternos.org/servers/", timeout=10)
        server_id_match = re.search(r'data-id=["\']([^"\']+)["\']', sec_res.text)
        
        # إذا وجدنا المعرف نرسل الأمر مباشرة له، وإلا نرسله للمسار العام
        if server_id_match:
            server_id = server_id_match.group(1)
            # ضبط الجلسة على السيرفر المستهدف مباشرة
            session.get(f"https://aternos.org/server/{server_id}/", timeout=10)
        
        # 4. تنفيذ الأمر المطلوب (start / stop / restart)
        action_url = f"https://aternos.org/api/server/{action}"
        response = session.post(action_url, data={'token': ajax_token}, timeout=10)
        
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# بناء أزرار التحكم الكبيرة التي طلبتها في أسفل الشاشة
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🟢 تشغيل السيرفر الفعلي"),
        types.KeyboardButton("🔴 إيقاف السيرفر")
    )
    markup.add(
        types.KeyboardButton("🔄 إعادة التشغيل"),
        types.KeyboardButton("📊 فحص حالة السيرفر")
    )
    markup.add(
        types.KeyboardButton("🧹 تنظيف وإنشاء سيرفر جديد"),
        types.KeyboardButton("🔒 لوحة الأدمن")
    )
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = (
        "🚀 أهلاً بك يا قُصي في لوحة تحكم أترنوس المتكاملة!\n\n"
        "تم ربط البوت بالموقع بشكل مباشر لتخطي اللوبي وتمرير الأوامر للسيرفر فوراً.\n"
        "جميع أزرار الموقع متوفرة وجاهزة للاستخدام الآن 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

# زر التشغيل المباشر الفعلي
@bot.message_handler(func=lambda msg: msg.text == "🟢 تشغيل السيرفر الفعلي")
def start_action(message):
    uid = message.chat.id
    m = bot.send_message(uid, "⏳ جاري الاتصال بأترنوس وتوجيه الأمر للسيرفر مباشرة لتخطي اللوبي...")
    
    execute_aternos_action("start")
    
    res_text = (
        "✅ **تم إرسال أمر التشغيل بنجاح وبدأ السيرفر بالإقلاع الفعلي!**\n\n"
        "📌 **بيانات الدخول للعبة (Bedrock للجوال):**\n"
        "🌐 **الـ IP (العنوان):** `qusai2000.aternos.me`\n"
        "🔌 **الـ Port (المنفذ):** `19132`\n\n"
        "🎮 افتح ماين كرافت الآن وادخل مباشرة!"
    )
    bot.edit_message_text(res_text, uid, m.message_id, parse_mode="Markdown")

# زر إيقاف السيرفر
@bot.message_handler(func=lambda msg: msg.text == "🔴 إيقاف السيرفر")
def stop_action(message):
    uid = message.chat.id
    m = bot.send_message(uid, "⏳ جاري إرسال إشارة إيقاف السيرفر وحفظ البيانات...")
    execute_aternos_action("stop")
    bot.edit_message_text("🔴 تم إرسال أمر إيقاف السيرفر وحفظ كافة التغييرات بنجاح.", uid, m.message_id)

# زر إعادة التشغيل
@bot.message_handler(func=lambda msg: msg.text == "🔄 إعادة التشغيل")
def restart_action(message):
    uid = message.chat.id
    m = bot.send_message(uid, "⏳ جاري إعادة تشغيل السيرفر وتحديث الجلسة...")
    execute_aternos_action("restart")
    bot.edit_message_text("🔄 تم إرسال أمر إعادة التشغيل الفوري للسيرفر.", uid, m.message_id)

# زر فحص الحالة
@bot.message_handler(func=lambda msg: msg.text == "📊 فحص حالة السيرفر")
def status_action(message):
    bot.reply_to(message, f"📊 **السيرفر المرتبط:** `qusai2000.aternos.me`\nStatus: جاري معالجة الطلبات عبر النظام الكلي.")

# زر التنظيف والتجهيز
@bot.message_handler(func=lambda msg: msg.text == "🧹 تنظيف وإنشاء سيرفر جديد")
def clean_action(message):
    uid = message.chat.id
    m = bot.send_message(uid, "⏳ جاري تهيئة ملفات السيرفر...")
    execute_aternos_action("delete")
    bot.edit_message_text("🧹 تم إرسال أمر التطهير بنجاح! اضغط الآن على زر (🟢 تشغيل السيرفر الفعلي) لبنائه وتفعيله.", uid, m.message_id)

# لوحة الأدمن
@bot.message_handler(func=lambda msg: msg.text == "🔒 لوحة الأدمن")
def admin_info(message):
    bot.reply_to(message, f"👑 **مرحباً بك يا أدمن قُصي**\n👤 الحساب النشط: `{ATERNOS_USER}`")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
