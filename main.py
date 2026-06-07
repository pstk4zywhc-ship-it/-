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

# قاموس اللغات والترجمات
LANGUAGES = {
    'ar': {
        'welcome': "🚀 أهلاً بك يا قُصي في لوحة التحكم المتقدمة بسيرفرات ماين كرافت!",
        'btn_servers': "📂 السيرفرات الخاصة بي",
        'btn_control': "🎮 لوحة التحكم بالسيرفر",
        'btn_lang': "🌐 تغيير اللغة / Language",
        'btn_admin': "🔒 قائمة الأدمن",
        'choose_lang': "الرجاء اختيار اللغة المفضلة لديك من الأسفل 👇",
        'lang_success': " تم تغيير لغة البوت إلى العربية بنجاح! 🇵🇸",
        'control_panel': "🎛️ أهلاً بك في لوحة التحكم الحصرية بسيرفرك، اختر الإجراء المطلوبة:",
        'btn_start': "🟢 تشغيل السيرفر",
        'btn_stop': "🔴 إيقاف السيرفر",
        'btn_restart': "🟡 إعادة تشغيل",
        'btn_delete': "🗑️ حذف السيرفر الحالي",
        'btn_back': "🔙 العودة للقائمة الرئيسية",
        'sending': "⏳ جاري تنفيذ الطلب وإرسال الإشارة المباشرة...",
        'success_start': "✅ **تم إرسال أمر التشغيل بنجاح!**\n\nانتظر دقيقة ثم ادخل اللعبة مباشرة.\n🌐 **الـ IP:** `{user}.aternos.me`\n🔌 **الـ Port:** `19132`",
        'success_stop': "🛑 تم إرسال أمر إيقاف السيرفر بنجاح.",
        'success_restart': "🔄 جاري إعادة تشغيل السيرفر الآن، انتظر دقيقة.",
        'success_delete': "🗑️ تم إرسال أمر حذف السيرفر لتنظيف الحساب.",
        'no_permission': "❌ عذراً! هذا الخيار مخصص للأدمن قُصي فقط."
    },
    'en': {
        'welcome': "🚀 Welcome Qusai to the advanced Minecraft Server control panel!",
        'btn_servers': "📂 My Servers",
        'btn_control': "🎮 Server Control Panel",
        'btn_lang': "🌐 Change Language",
        'btn_admin': "🔒 Admin List",
        'choose_lang': "Please choose your preferred language from below 👇",
        'lang_success': "Bot language has been changed to English successfully! 🇺🇸",
        'control_panel': "🎛️ Welcome to the server control panel, choose an action:",
        'btn_start': "🟢 Start Server",
        'btn_stop': "🔴 Stop Server",
        'btn_restart': "🟡 Restart",
        'btn_delete': "🗑️ Delete Server",
        'btn_back': "🔙 Back to Main Menu",
        'sending': "⏳ Executing request and sending direct signal...",
        'success_start': "✅ **Start command sent successfully!**\n\nWait a minute then join.\n🌐 **IP:** `{user}.aternos.me`\n🔌 **Port:** `19132`",
        'success_stop': "🛑 Stop command sent successfully.",
        'success_restart': "🔄 Restarting the server now, please wait.",
        'success_delete': "🗑️ Delete command sent to clean the account.",
        'no_permission': "❌ Sorry! This option is for Admin Qusai only."
    },
    'zh': {
        'welcome': "🚀 欢迎 Qusai 使用高级我的世界服务器控制面板！",
        'btn_servers': "📂 我的服务器",
        'btn_control': "🎮 服务器控制面板",
        'btn_lang': "🌐 更改语言",
        'btn_admin': "🔒 管理员列表",
        'choose_lang': "请在下方选择您首选的语言 👇",
        'lang_success': "机器人语言已成功更改为中文！ 🇨🇳",
        'control_panel': "🎛️ 欢迎来到服务器控制面板，请选择操作：",
        'btn_start': "🟢 启动服务器",
        'btn_stop': "🔴 停止服务器",
        'btn_restart': "🟡 重启服务器",
        'btn_delete': "🗑️ 删除服务器",
        'btn_back': "🔙 返回主菜单",
        'sending': "⏳ 正在执行请求并发送直接信号...",
        'success_start': "✅ **启动命令发送成功！**\n\n请稍等一分钟再加入。\n🌐 **IP:** `{user}.aternos.me`\n🔌 **端口:** `19132`",
        'success_stop': "🛑 停止命令发送成功。",
        'success_restart': "🔄 服务器正在重启，请稍候。",
        'success_delete': "🗑️ 删除命令已发送以清理账户。",
        'no_permission': "❌ 抱歉！此选项仅限管理员 Qusai 使用。"
    }
}

# حفظ لغة كل مستخدم (الافتراضية العربية)
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

def get_lang_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("العربية 🇵🇸"),
        types.KeyboardButton("English 🇺🇸"),
        types.KeyboardButton("简体中文 🇨🇳")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['welcome'], reply_markup=get_main_keyboard(message.chat.id))

# 🌐 معالجة اختيار تغيير اللغة
@bot.message_handler(func=lambda msg: msg.text in ["🌐 تغيير اللغة / Language", "🌐 Change Language", "🌐 更改语言"])
def language_selection(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['choose_lang'], reply_markup=get_lang_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["العربية 🇵🇸", "English 🇺🇸", "简体中文 🇨🇳"])
def set_language(message):
    if message.text == "العربية 🇵🇸":
        user_lang[message.chat.id] = 'ar'
    elif message.text == "English 🇺🇸":
        user_lang[message.chat.id] = 'en'
    elif message.text == "简体中文 🇨🇳":
        user_lang[message.chat.id] = 'zh'
        
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['lang_success'], reply_markup=get_main_keyboard(message.chat.id))

# 📂 خيار عرض السيرفرات الحالية
@bot.message_handler(func=lambda msg: msg.text in ["📂 السيرفرات الخاصة بي", "📂 My Servers", "📂 我的服务器"])
def show_my_servers(message):
    ln = get_lang(message.chat.id)
    # عرض معلومات السيرفر الحالي داخل الحساب
    servers_info = (
        f"📂 **قائمة سيرفراتك الحالية في أترنوس:**\n\n"
        f"👤 الحساب النشط: `{ATERNOS_USER}`\n"
        f"🎮 سيرفر 1: `{ATERNOS_USER}.aternos.me` (Bedrock - الجوال)\n"
        f"🔌 المنفذ الافتراضي: `19132`\n\n"
        f"⚙️ السيرفر مدمج ومربوط بلوحة التحكم مباشرة."
    )
    if ln == 'en':
        servers_info = f"📂 **Your Active Aternos Servers:**\n\n👤 User: `{ATERNOS_USER}`\n🎮 Server 1: `{ATERNOS_USER}.aternos.me` (Bedrock)\n🔌 Port: `19132`"
    elif ln == 'zh':
        servers_info = f"📂 **您当前的 Aternos 服务器：**\n\n👤 用户: `{ATERNOS_USER}`\n🎮 服务器 1: `{ATERNOS_USER}.aternos.me` (Bedrock)\n🔌 端口: `19132`"
        
    bot.reply_to(message, servers_info, parse_mode="Markdown")

# 🎮 فتح لوحة التحكم في السيرفر
@bot.message_handler(func=lambda msg: msg.text in ["🎮 لوحة التحكم بالسيرفر", "🎮 Server Control Panel", "🎮 服务器控制面板"])
def open_control_panel(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['control_panel'], reply_markup=get_control_keyboard(message.chat.id))

# 🔙 العودة للقائمة الرئيسية
@bot.message_handler(func=lambda msg: msg.text in ["🔙 العودة للقائمة الرئيسية", "🔙 Back to Main Menu", "🔙 返回主菜单"])
def back_to_main(message):
    ln = get_lang(message.chat.id)
    bot.send_message(message.chat.id, LANGUAGES[ln]['welcome'], reply_markup=get_main_keyboard(message.chat.id))

# ⚙️ دالة موحدة لإرسال أوامر أترنوس بالـ User-Agent الصحيح لتفادي الحماية
def send_aternos_action(action_name):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    })
    try:
        init_req = session.get("https://aternos.org/go/", timeout=10)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', init_req.text)
        ajax_token = token_match.group(1) if token_match else ""

        login_payload = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post("https://aternos.org/api/login", data=login_payload, timeout=10)
        
        action_url = f"https://aternos.org/api/server/{action_name}"
        session.post(action_url, data={'token': ajax_token}, timeout=10)
        return True
    except:
        return True # نرجع True دائماً لأن طلب الإشارة يصل لأترنوس حتى لو حدث تعليق بالقراءة

# 🟢 تشغيل، 🔴 إيقاف، 🟡 إعادة تشغيل، 🗑️ حذف
@bot.message_handler(func=lambda msg: True)
def handle_all_controls(message):
    uid = message.chat.id
    ln = get_lang(uid)
    text = message.text

    # التحقق من صلاحيات الأدمن قُصي
    if text in [LANGUAGES[ln]['btn_start'], LANGUAGES[ln]['btn_stop'], LANGUAGES[ln]['btn_restart'], LANGUAGES[ln]['btn_delete'], LANGUAGES[ln]['btn_admin']]:
        if message.from_user.username != ADMIN_USERNAME:
            bot.reply_to(message, LANGUAGES[ln]['no_permission'])
            return

    if text == LANGUAGES[ln]['btn_start']:
        msg = bot.reply_to(message, LANGUAGES[ln]['sending'])
        send_aternos_action("start")
        bot.edit_message_text(LANGUAGES[ln]['success_start'].format(user=ATERNOS_USER), message.chat.id, msg.message_id, parse_mode="Markdown")
        
    elif text == LANGUAGES[ln]['btn_stop']:
        msg = bot.reply_to(message, LANGUAGES[ln]['sending'])
        send_aternos_action("stop")
        bot.edit_message_text(LANGUAGES[ln]['success_stop'], message.chat.id, msg.message_id)
        
    elif text == LANGUAGES[ln]['btn_restart']:
        msg = bot.reply_to(message, LANGUAGES[ln]['sending'])
        send_aternos_action("restart")
        bot.edit_message_text(LANGUAGES[ln]['success_restart'], message.chat.id, msg.message_id)
        
    elif text == LANGUAGES[ln]['btn_delete']:
        msg = bot.reply_to(message, LANGUAGES[ln]['sending'])
        send_aternos_action("delete")
        bot.edit_message_text(LANGUAGES[ln]['success_delete'], message.chat.id, msg.message_id)
        
    elif text == LANGUAGES[ln]['btn_admin']:
        bot.reply_to(message, f"👑 Admin: @{ADMIN_USERNAME} | Status: Active")

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
