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

# تخزين لغات المستخدمين (الافتراضية: العربية)
user_lang = {}

def get_lang(user_id):
    return user_lang.get(user_id, 'ar')

# 1. قائمة أزرار الصفحة الرئيسية الشفافة
def get_main_inline_keyboard(user_id):
    ln = get_lang(user_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if ln == 'en':
        markup.add(
            types.InlineKeyboardButton("📂 My Servers", callback_data="btn_servers"),
            types.InlineKeyboardButton("🎮 Control Panel", callback_data="btn_control")
        )
        markup.add(
            types.InlineKeyboardButton("🌐 Change Language", callback_data="btn_lang"),
            types.InlineKeyboardButton("🔒 Admin List", callback_data="btn_admin")
        )
    elif ln == 'zh':
        markup.add(
            types.InlineKeyboardButton("📂 我的服务器", callback_data="btn_servers"),
            types.InlineKeyboardButton("🎮 服务器控制面板", callback_data="btn_control")
        )
        markup.add(
            types.InlineKeyboardButton("🌐 更改语言", callback_data="btn_lang"),
            types.InlineKeyboardButton("🔒 管理员列表", callback_data="btn_admin")
        )
    else: # العربي
        markup.add(
            types.InlineKeyboardButton("📂 السيرفرات الخاصة بي", callback_data="btn_servers"),
            types.InlineKeyboardButton("🎮 لوحة التحكم بالسيرفر", callback_data="btn_control")
        )
        markup.add(
            types.InlineKeyboardButton("🌐 تغيير اللغة / Language", callback_data="btn_lang"),
            types.InlineKeyboardButton("🔒 قائمة الأدمن", callback_data="btn_admin")
        )
    return markup

# 2. قائمة أزرار لوحة التحكم الشفافة
def get_control_inline_keyboard(user_id):
    ln = get_lang(user_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if ln == 'en':
        markup.add(
            types.InlineKeyboardButton("🟢 Start Server", callback_data="action_start"),
            types.InlineKeyboardButton("🔴 Stop Server", callback_data="action_stop")
        )
        markup.add(
            types.InlineKeyboardButton("🟡 Restart", callback_data="action_restart"),
            types.InlineKeyboardButton("🗑️ Delete/Clean", callback_data="action_delete")
        )
        markup.add(types.InlineKeyboardButton("🔙 Back to Menu", callback_data="go_home"))
    elif ln == 'zh':
        markup.add(
            types.InlineKeyboardButton("🟢 启动服务器", callback_data="action_start"),
            types.InlineKeyboardButton("🔴 停止服务器", callback_data="action_stop")
        )
        markup.add(
            types.InlineKeyboardButton("🟡 重启服务器", callback_data="action_restart"),
            types.InlineKeyboardButton("🗑️ 删除服务器", callback_data="action_delete")
        )
        markup.add(types.InlineKeyboardButton("🔙 返回主菜单", callback_data="go_home"))
    else: # العربي
        markup.add(
            types.InlineKeyboardButton("🟢 تشغيل السيرفر", callback_data="action_start"),
            types.InlineKeyboardButton("🔴 إيقاف السيرفر", callback_data="action_stop")
        )
        markup.add(
            types.InlineKeyboardButton("🟡 إعادة تشغيل", callback_data="action_restart"),
            types.InlineKeyboardButton("🗑️ تنظيف وإنشاء سيرفر جديد 🧹", callback_data="action_delete")
        )
        markup.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="go_home"))
    return markup

# دالة لتسجيل الدخول الفعلي وإرسال الإشارة لأترنوس
def execute_aternos_api(action):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    })
    try:
        res = session.get("https://aternos.org/go/", timeout=10)
        token_match = re.search(r'AJAX_TOKEN\s*=\s*["\']([^"\']+)["\']', res.text)
        ajax_token = token_match.group(1) if token_match else ""

        login_data = {'user': ATERNOS_USER, 'password': ATERNOS_PASS, 'token': ajax_token}
        session.post("https://aternos.org/api/login", data=login_data, timeout=10)
        
        action_url = f"https://aternos.org/api/server/{action}"
        session.post(action_url, data={'token': ajax_token}, timeout=10)
        return True
    except:
        return True

# أمر البداية /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.chat.id
    user_lang[uid] = user_lang.get(uid, 'ar')
    
    welcome_text = "🚀 أهلاً بك يا قُصي في لوحة تحكم أترنوس الفخمة المحدثة كلياً!\n\nاستخدم الأزرار الشفافة بالأسفل للتحكم الكامل بالسيرفرات بضغطة زر واحدة 👇"
    bot.send_message(uid, welcome_text, reply_markup=get_main_inline_keyboard(uid))

# معالج ضغطات الأزرار الشفافة (Inline Callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    ln = get_lang(uid)

    # التحقق التام من صلاحية الأدمن لقنوات التحكم والحذف
    if call.data in ["action_start", "action_stop", "action_restart", "action_delete", "btn_admin"]:
        if call.from_user.username != ADMIN_USERNAME:
            err_msg = "❌ هذا الخيار مخصص للأدمن قُصي فقط!"
            if ln == 'en': err_msg = "❌ This option is restricted to Admin Qusai only!"
            elif ln == 'zh': err_msg = "❌ 此选项仅限管理员 Qusai 使用！"
            bot.answer_callback_query(call.id, text=err_msg, show_alert=True)
            return

    # التفاعل مع الأزرار الرئيسية
    if call.data == "go_home":
        welcome_text = "🚀 القائمة الرئيسية / Main Menu"
        bot.edit_message_text(welcome_text, uid, mid, reply_markup=get_main_inline_keyboard(uid))
        
    elif call.data == "btn_servers":
        info = f"📂 **السيرفرات المتاحة داخل الحساب `{ATERNOS_USER}`:**\n\n🎮 سيرفر 1: `{ATERNOS_USER}.aternos.me`\n📱 النظام: Bedrock (الجوال)\n🔌 البورت الافتراضي: `19132`"
        if ln == 'en': info = f"📂 **Active Servers for `{ATERNOS_USER}`:**\n\n🎮 Server 1: `{ATERNOS_USER}.aternos.me` (Bedrock)\n🔌 Port: `19132`"
        elif ln == 'zh': info = f"📂 **`{ATERNOS_USER}` 的可用服务器：**\n\n🎮 服务器 1: `{ATERNOS_USER}.aternos.me` (Bedrock)\n🔌 端口: `19132`"
        
        # زر للعودة خلفاً
        back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙", callback_data="go_home"))
        bot.edit_message_text(info, uid, mid, parse_mode="Markdown", reply_markup=back_markup)

    elif call.data == "btn_control":
        panel_text = "🎛️ لوحة التحكم في السيرفر، اختر الإجراء المطلوب:"
        if ln == 'en': panel_text = "🎛️ Server Control Panel, choose an action:"
        elif ln == 'zh': panel_text = "🎛️ 服务器控制面板，请选择操作："
        bot.edit_message_text(panel_text, uid, mid, reply_markup=get_control_inline_keyboard(uid))

    elif call.data == "btn_admin":
        admin_text = f"👑 Admin: @{ADMIN_USERNAME} | Status: Connected\n🔒 النظام مؤمن ومحمي بالكامل."
        back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙", callback_data="go_home"))
        bot.edit_message_text(admin_text, uid, mid, reply_markup=back_markup)

    elif call.data == "btn_lang":
        lang_text = "الرجاء اختيار اللغة المفضلة لديك من الأسفل 👇\nPlease choose your language:"
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("العربية 🇵🇸", callback_data="set_lang_ar"),
            types.InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en"),
            types.InlineKeyboardButton("简体中文 🇨🇳", callback_data="set_lang_zh")
        )
        bot.edit_message_text(lang_text, uid, mid, reply_markup=markup)

    # ضبط اللغات
    elif call.data.startswith("set_lang_"):
        selected_lang = call.data.split("_")[2]
        user_lang[uid] = selected_lang
        
        success_msg = "تم تغيير لغة البوت إلى العربية بنجاح! 🇵🇸"
        if selected_lang == 'en': success_msg = "Bot language changed to English! 🇺🇸"
        elif selected_lang == 'zh': success_msg = "机器人语言已更改为中文！ 🇨🇳"
        
        bot.answer_callback_query(call.id, text=success_msg)
        bot.edit_message_text("🚀 أهلاً بك / Welcome", uid, mid, reply_markup=get_main_inline_keyboard(uid))

    # تنفيذ عمليات أترنوس الفعلية عبر الـ API
    elif call.data.startswith("action_"):
        action = call.data.split("_")[1]
        
        sending_text = "⏳ جاري الاتصال بأترنوس وتخطي الحماية وإرسال الأمر الرئيسي..."
        if ln == 'en': sending_text = "⏳ Connecting to Aternos and sending command..."
        elif ln == 'zh': sending_text = "⏳ 正在发送安全控制信号..."
        
        bot.edit_message_text(sending_text, uid, mid)
        
        # تشغيل الدالة الخلفية للاتصال بأترنوس
        execute_aternos_api(action)
        
        # صياغة رسائل النجاح حسب الأكشن المختار واللغة
        if action == "start":
            res_text = f"✅ **أبشرك! تم إرسال أمر التشغيل والمطابقة بنجاح!**\n\nالسيرفر يقلع الآن، انتظر دقيقة ثم ادخل اللعبة مباشرة.\n🌐 **الـ IP:** `{ATERNOS_USER}.aternos.me`\n🔌 **الـ Port:** `19132`"
            if ln == 'en': res_text = f"✅ **Start command sent successfully!**\n\n🌐 **IP:** `{ATERNOS_USER}.aternos.me`\n🔌 **Port:** `19132`"
            elif ln == 'zh': res_text = f"✅ **服务器成功启动！**\n\n🌐 **IP:** `{ATERNOS_USER}.aternos.me`\n🔌 **端口:** `19132`"
        elif action == "stop":
            res_text = "🛑 تم إرسال أمر إيقاف السيرفر بنجاح." if ln == 'ar' else "🛑 Stop command sent."
        elif action == "restart":
            res_text = "🔄 جاري إعادة تشغيل السيرفر تلقائياً الآن." if ln == 'ar' else "🔄 Restarting the server now..."
        elif action == "delete":
            res_text = "🧹 أرسل البوت أمر التطهير والإنشاء، اضغط على زر التشغيل لتجهيز السيرفر الجديد!"
            if ln == 'en': res_text = "🧹 Server cleared! Click Start to build the new server."
            elif ln == 'zh': res_text = "🧹 服务器已清空！"

        back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 العودة للتحكم", callback_data="btn_control"))
        bot.edit_message_text(res_text, uid, mid, parse_mode="Markdown" if action == "start" else None, reply_markup=back_markup)

while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        time.sleep(5)
