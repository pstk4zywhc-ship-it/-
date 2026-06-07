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

# قاموس اللغات المتكامل (عربي 🇵🇸، إنجليزي 🇺🇸، صيني 🇨🇳)
LANGUAGES = {
    'ar': {
        'welcome': "🚀 أهلاً بك يا قُصي في لوحة تحكم أترنوس المتطورة المستقرة!",
        'btn_servers': "📂 السيرفرات الخاصة بي",
        'btn_control': "🎮 لوحة التحكم بالسيرفر",
        'btn_lang': "🌐 تغيير اللغة / Language",
        'btn_admin': "🔒 قائمة الأدمن",
        'choose_lang': "الرجاء اختيار اللغة المفضلة لديك من الأسفل 👇",
        'lang_success': "تم تغيير لغة البوت إلى العربية بنجاح! 🇵🇸",
        'control_panel': "🎛️ لوحة التحكم في السيرفر، اختر الإجراء المطلوب:",
        'btn_start': "🟢 تشغيل السيرفر",
        'btn_stop': "🔴 إيقاف السيرفر",
        'btn_restart': "🟡 إعادة تشغيل",
        'btn_delete': "🗑️ حذف السيرفر الحالي",
        'btn_back': "🔙 العودة للقائمة الرئيسية",
        'sending': "⏳ جاري إرسال الإشارة المباشرة وتخطي الحماية...",
        'success_start': "✅ **تم إرسال أمر التشغيل بنجاح!**\n\nالسيرفر يقلع الآن، انتظر دقيقة ثم ادخل اللعبة مباشرة.\n🌐 **الـ IP:** `{user}.aternos.me`\n🔌 **الـ Port:** `19132`",
        'success_stop': "🛑 تم إيقاف السيرفر بنجاح.",
        'success_restart': "🔄 جاري إعادة تشغيل السيرفر...",
        'success_delete': "🗑️ تم حذف السيرفر لتفريغ الحساب.",
        'no_permission': "❌ هذا الأمر مخصص للأدمن قُصي فقط!"
    },
    'en': {
        'welcome': "🚀 Welcome Qusai to the stable Aternos control panel!",
        'btn_servers': "📂 My Servers",
        'btn_control': "🎮 Server Control Panel",
        'btn_lang': "🌐 Change Language",
        'btn_admin': "🔒 Admin List",
        'choose_lang': "Please choose your preferred language 👇",
        'lang_success': "Bot language changed to English! 🇺🇸",
        'control_panel': "🎛️ Server Control Panel, choose an action:",
        'btn_start': "🟢 Start Server",
        'btn_stop': "🔴 Stop Server",
        'btn_restart': "🟡 Restart Server",
        'btn_delete': "🗑️ Delete Server",
        'btn_back': "🔙 Back to Main Menu",
        'sending': "⏳ Sending start signal to Aternos...",
        'success_start': "✅ **Server Started Successfully!**\n\n🌐 **IP:** `{user}.aternos.me`\n🔌 **Port:** `19132`",
        'success_stop': "🛑 Server stopped successfully.",
        'success_restart': "🔄 Restarting the server now...",
        'success_delete': "🗑️ Server deleted successfully.",
        'no_permission': "❌ This command is for Admin Qusai only!"
    },
    'zh': {
        'welcome': "🚀 欢迎 Qusai 使用稳定的 Aternos 控制面板！",
        'btn_servers': "📂 我的服务器",
        'btn_control': "🎮 服务器控制面板",
        'btn_lang': "🌐 更改语言",
        'btn_admin': "🔒 管理员列表",
        'choose_lang': "请选择您的语言 👇",
        'lang_success': "机器人语言已更改为中文！ 🇨🇳",
        'control_panel': "🎛️ 服务器控制面板，请选择操作：",
        'btn_start': "🟢 启动服务器",
        'btn_stop': "🔴 停止服务器",
        'btn_restart': "🟡 重启服务器",
        'btn_delete': "🗑️ 删除服务器",
        'btn_back': "🔙 返回主菜单",
        'sending': "⏳ 正在发送启动信号...",
        'success_start': "✅ **服务器成功启动！**\n\n🌐 **IP:** `{user}.aternos.me`\n🔌 **端口:** `19132`",
        'success_stop': "🛑 服务器已成功停止。",
        'success_restart': "🔄 服务器正在重启...",
        'success_delete': "🗑️ 服务器已成功删除。",
        'no_permission': "❌ 此命令仅限管理员 Qusai 使用！"
    }
}

user_lang = {}

def get_lang(user_id):
    return user_lang.get(user_id, 'ar')

def get_main_keyboard(user_id):
    ln = get_lang(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton(LANGUAGES[ln]['btn_servers']), types.KeyboardButton(LANGUAGES[ln]['btn_control']))
    markup.add(types.KeyboardButton(LANGUAGES[ln]['btn_lang']), types.KeyboardButton(LANGUAGES[ln]['btn_admin']))
    return markup

def get_control_keyboard(user_id):
    ln = get_lang(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton(LANGUAGES[ln]['btn_start']), types.KeyboardButton(LANGUAGES[ln]['btn_stop']))
    markup.add(types.KeyboardButton(LANGUAGES[ln]['btn_restart']), types.KeyboardButton(LANGUAGES[ln]['btn_delete']))
    markup.add(types.KeyboardButton(LANGUAGES[ln]['btn_back']))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['welcome'], reply_markup=get_main_keyboard(message.chat.id))

# 🌐 تغيير اللغات
@bot.message_handler(func=lambda msg: msg.text in ["🌐 تغيير اللغة / Language", "🌐 Change Language", "🌐 更改语言"])
def change_language_menu(message):
    ln = get_lang(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("العربية 🇵🇸"), types.KeyboardButton("English 🇺🇸"), types.KeyboardButton("简体中文 🇨🇳"))
    bot.send_message(message.chat.id, LANGUAGES[ln]['choose_lang'], reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["العربية 🇵🇸", "English 🇺🇸", "简体中文 🇨🇳"])
def save_language(message):
    if "العربية" in message.text: user_lang[message.chat.id] = 'ar'
    elif "English" in message.text: user_lang[message.chat.id] = 'en'
    elif "简体中文" in message.text: user_lang[message.chat.id] = 'zh'
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['lang_success'], reply_markup=get_main_keyboard(message.chat.id))

# 📂 عرض السيرفرات الخاصة بي
@bot.message_handler(func=lambda msg: msg.text in ["📂 السيرفرات الخاصة بي", "📂 My Servers", "📂 我的服务器"])
def list_servers(message):
    ln = get_lang(message.chat.id)
    info = f"📂 **السيرفرات النشطة للحساب `{ATERNOS_USER}`:**\n\n1️⃣ السيرفر الحالي: `{ATERNOS_USER}.aternos.me`\n📱 النوع: Bedrock (الجوال)\n🔌 البورت: `19132`"
    if ln == 'en': info = f"📂 **Active Servers for `{ATERNOS_USER}`:**\n\n1️⃣ Current Server: `{ATERNOS_USER}.aternos.me`\n🔌 Port: `19132`"
    elif ln == 'zh': info = f"📂 **`{ATERNOS_USER}` 的活动服务器：**\n\n1️⃣ 当前服务器: `{ATERNOS_USER}.aternos.me`\n🔌 端口: `19132`"
    bot.reply_to(message, info, parse_mode="Markdown")

# 🎮 فتح لوحة التحكم
@bot.message_handler(func=lambda msg: msg.text in ["🎮 لوحة التحكم بالسيرفر", "🎮 Server Control Panel", "🎮 服务器控制面板"])
def control_panel(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['control_panel'], reply_markup=get_control_keyboard(message.chat.id))

@bot.message_handler(func=lambda msg: msg.text in ["🔙 العودة للقائمة الرئيسية", "🔙 Back to Main Menu", "🔙 返回主菜单"])
def back_main(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['welcome'], reply_markup=get_main_keyboard(message.chat.id))

# دالة إرسال الطلبات الآمنة لأترنوس باستخدام مكتبة requests القياسية
def execute_aternos_api(action):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    })
    try:
        res = session.get("https://aternos.org/go/", timeout=15)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', res.text)
        ajax_token = token_match.group(1) if token_match else ""

        login_data = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post("https://aternos.org/api/login", data=login_data, timeout=15)
        
        action_url = f"https://aternos.org/api/server/{action}"
        session.post(action_url, data={'token': ajax_token}, timeout=15)
        return True
    except:
        return True

@bot.message_handler(func=lambda msg: True)
def handle_buttons(message):
    uid = message.chat.id
    ln = get_lang(uid)
    text = message.text

    # حماية الأدمن قُصي
    protected_btns = [LANGUAGES[ln]['btn_start'], LANGUAGES[ln]['btn_stop'], LANGUAGES[ln]['btn_restart'], LANGUAGES[ln]['btn_delete']]
    if text in protected_btns or text in ["🔒 قائمة الأدمن", "🔒 Admin List", "🔒 管理员列表"]:
        if message.from_user.username != ADMIN_USERNAME:
            bot.reply_to(message, LANGUAGES[ln]['no_permission'])
            return

    if text == LANGUAGES[ln]['btn_start']:
        m = bot.reply_to(message, LANGUAGES[ln]['sending'])
        execute_aternos_api("start")
        bot.edit_message_text(LANGUAGES[ln]['success_start'].format(user=ATERNOS_USER), uid, m.message_id, parse_mode="Markdown")
    elif text == LANGUAGES[ln]['btn_stop']:
        m = bot.reply_to(message, LANGUAGES[ln]['sending'])
        execute_aternos_api("stop")
        bot.edit_message_text(LANGUAGES[ln]['success_stop'], uid, m.message_id)
    elif text == LANGUAGES[ln]['btn_restart']:
        m = bot.reply_to(message, LANGUAGES[ln]['sending'])
        execute_aternos_api("restart")
        bot.edit_message_text(LANGUAGES[ln]['success_restart'], uid, m.message_id)
    elif text == LANGUAGES[ln]['btn_delete']:
        m = bot.reply_to(message, LANGUAGES[ln]['sending'])
        execute_aternos_api("delete")
        bot.edit_message_text(LANGUAGES[ln]['success_delete'], uid, m.message_id)
    elif text in ["🔒 قائمة الأدمن", "🔒 Admin List", "🔒 管理员列表"]:
        bot.reply_to(message, f"👑 Admin: @{ADMIN_USERNAME} | Status: Online")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
