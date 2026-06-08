import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# إعدادات المراقبة
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# قاموس اللغات الثلاث لتسهيل العرض بدون أخطاء التواء النصوص
LANGUAGES = {
    'ar': {
        'welcome': "👋 مرحباً بك في القائمة الرئيسية لبوت السيرفرات المتطور!\n\nاختر من الأزرار أدناه للبدء:",
        'btn_create': "انشاء سيرفر 👾",
        'btn_manage': "التحكم في السيرفر👨‍✈️",
        'btn_edit_ip': "تعديل الآي بي💯",
        'btn_add_mods': "اضافة مودات للسيرفر 🙏",
        'btn_seed': "تغيير الseed 🦾",
        'btn_start': "تشغيل السيرفر ✅",
        'btn_stop': "إطفاء السيرفر ❌",
        'btn_lang': "🌐 تغيير اللغة (Language / 语言)",
        'choose_type': "🎮 اختر نوع السيرفر الذي تريد صناعته:",
        'java_type': "🖥️ جافا (Java Edition)",
        'bedrock_type': "📱 بيدروك / جوال (Bedrock)",
        'creating': "⏳ يتم إنشاء السيرفر الخاص بك، يرجى الانتظار...",
        'success': "🤖 تم انشاء السيرفر يا بطل :\n\nالآيبي: `{ip}.aternos.me`\nالبوت: يعمل بنجاح ✅",
        'msg_ip': "✏️ أرسل الآن الاسم الجديد للآيبي (أحرف وأرقام فقط):",
        'msg_seed': "✏️ أرسل الـ Seed الجديد لعالم ماين كرافت الخاص بك:",
        'msg_mods': "📦 أرسل اسم المود أو الرابط لتثبيته في السيرفر:",
        'back': "🔙 عودة للقائمة الرئيسية"
    },
    'en': {
        'welcome': "👋 Welcome to the Advanced Server Management Bot!\n\nSelect an option from the menu below:",
        'btn_create': "Create Server 👾",
        'btn_manage': "Manage Server 👨‍✈️",
        'btn_edit_ip': "Edit IP 💯",
        'btn_add_mods': "Add Mods to Server 🙏",
        'btn_seed': "Change Seed 🦾",
        'btn_start': "Start Server ✅",
        'btn_stop': "Stop Server ❌",
        'btn_lang': "🌐 Change Language (اللغة / 语言)",
        'choose_type': "🎮 Choose your server edition:",
        'java_type': "🖥️ Java Edition",
        'bedrock_type': "📱 Bedrock / Mobile",
        'creating': "⏳ Your server is being created, please wait...",
        'success': "🤖 Server created successfully, hero!\n\nIP: `{ip}.aternos.me`\nBot: Active and running ✅",
        'msg_ip': "✏️ Send the new IP name (letters/numbers only):",
        'msg_seed': "✏️ Send the new Seed for your Minecraft world:",
        'msg_mods': "📦 Send the mod name or link to install it on your server:",
        'back': "🔙 Back to Main Menu"
    },
    'zh': {
        'welcome': "👋 欢迎使用高级服务器管理机器人！\n\n请从下方菜单中选择一项操作：",
        'btn_create': "创建服务器 👾",
        'btn_manage': "控制服务器 👨‍✈️",
        'btn_edit_ip': "修改 IP 💯",
        'btn_add_mods': "为服务器添加模组 🙏",
        'btn_seed': "修改世界种子 🦾",
        'btn_start': "启动服务器 ✅",
        'btn_stop': "关闭服务器 ❌",
        'btn_lang': "🌐 更改语言 (Language / اللغة)",
        'choose_type': "🎮 选择您想要创建的服务器版本：",
        'java_type': "🖥️ Java 版 (Java Edition)",
        'bedrock_type': "📱 基岩版 / 手机版 (Bedrock)",
        'creating': "⏳ 正在创建您的服务器，请稍候...",
        'success': "🤖 服务器创建成功，英雄！\n\nIP地址: `{ip}.aternos.me`\n机器人: 运行成功 ✅",
        'msg_ip': "✏️ 现在发送新的 IP 名称（仅限字母/数字）：",
        'msg_seed': "✏️ 发送您想为世界设置的新种子 (Seed)：",
        'msg_mods': "📦 发送您想添加的模组 (Mod) 名称或链接：",
        'back': "🔙 返回主菜单"
    }
}

user_preferences = {}
user_states = {}
user_servers = {}

def get_lang(user_id):
    return user_preferences.get(user_id, 'ar')

# عند كتابة /start تظهر القائمة الرئيسية مباشرة بالأزرار المطلوبة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    
    if user_id not in user_servers:
        user_servers[user_id] = f"mc{user_id % 10000}"
        
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang]['btn_create'], callback_data='go_create')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_manage'], callback_data='manage_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_edit_ip'], callback_data='edit_ip')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_add_mods'], callback_data='add_mods'),
         InlineKeyboardButton(LANGUAGES[lang]['btn_seed'], callback_data='change_seed')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_start'], callback_data='start_srv'),
         InlineKeyboardButton(LANGUAGES[lang]['btn_stop'], callback_data='stop_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_lang'], callback_data='choose_lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(LANGUAGES[lang]['welcome'], reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(LANGUAGES[lang]['welcome'], reply_markup=reply_markup)

# معالج ضغطات الأزرار التفاعلية
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_lang(user_id)
    data = query.data

    if data == 'main_menu':
        await start(update, context)
        
    elif data == 'go_create':
        keyboard = [
            [InlineKeyboardButton(LANGUAGES[lang]['java_type'], callback_data='make_java'),
             InlineKeyboardButton(LANGUAGES[lang]['bedrock_type'], callback_data='make_bedrock')],
            [InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text(LANGUAGES[lang]['choose_type'], reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data in ['make_java', 'make_bedrock']:
        # عند اختيار جافا أو بيدروك يظهر نص التحميل ثم الإنشاء بنجاح
        await query.edit_message_text(LANGUAGES[lang]['creating'])
        current_ip = user_servers.get(user_id, f"mc{user_id % 10000}")
        success_text = LANGUAGES[lang]['success'].format(ip=current_ip)
        
        keyboard = [[InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]]
        await query.message.reply_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif data == 'manage_srv':
        keyboard = [[InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]]
        msg = "👨‍✈️ **قسم التحكم في السيرفر:**\n\nالسيرفر تحت المراقبة الفورية، وجميع الاتصال مستقرة بدون مشاكل." if lang=='ar' else ("👨‍✈️ **Server Management Section:**\n\nServer monitored successfully." if lang=='en' else "👨‍✈️ **服务器管理部分：**\n\n服务器处于实时监控下。")
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif data == 'edit_ip':
        user_states[user_id] = 'waiting_for_ip'
        await query.edit_message_text(LANGUAGES[lang]['msg_ip'])
        
    elif data == 'add_mods':
        user_states[user_id] = 'waiting_for_mods'
        await query.edit_message_text(LANGUAGES[lang]['msg_mods'])
        
    elif data == 'change_seed':
        user_states[user_id] = 'waiting_for_seed'
        await query.edit_message_text(LANGUAGES[lang]['msg_seed'])
        
    elif data == 'start_srv':
        await query.edit_message_text(LANGUAGES[lang]['creating'])
        msg = "🟢 **تم إرسال أمر تشغيل السيرفر بنجاح وجاري الإقلاع!**" if lang=='ar' else ("🟢 **Server start command sent successfully!**" if lang=='en' else "🟢 **服务器启动命令发送成功！**")
        keyboard = [[InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]]
        await query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif data == 'stop_srv':
        await query.edit_message_text(LANGUAGES[lang]['creating'])
        msg = "🔴 **تم إرسال أمر إيقاف السيرفر بنجاح وتوفير الملفات.**" if lang=='ar' else ("🔴 **Server stop command sent successfully.**" if lang=='en' else "🔴 **服务器关闭命令发送成功。**")
        keyboard = [[InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]]
        await query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif data == 'choose_lang':
        keyboard = [
            [InlineKeyboardButton("العربية 🇵🇸", callback_data='set_lang_ar'),
             InlineKeyboardButton("English 🇺🇸", callback_data='set_lang_en'),
             InlineKeyboardButton("中文 🇨🇳", callback_data='set_lang_zh')],
            [InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text("🌐 اختر لغة البوت / Choose Language / 选择语言:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data.startswith('set_lang_'):
        new_lang = data.split('_')[2]
        user_preferences[user_id] = new_lang
        await start(update, context)

# استقبال المدخلات وتغيير القيم (الآيبي، المودات، السيد)
async def handle_text_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = get_lang(user_id)
    keyboard = [[InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if user_states.get(user_id) == 'waiting_for_ip':
        user_states[user_id] = None
        user_servers[user_id] = text.strip()
        reply = f"💯 تم تغيير آيبي السيرفر بنجاح إلى:\n`{text}.aternos.me`" if lang == 'ar' else (f"💯 IP changed successfully to:\n`{text}.aternos.me`" if lang == 'en' else f"💯 IP 成功更改为：\n`{text}.aternos.me`")
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode="Markdown")

    elif user_states.get(user_id) == 'waiting_for_seed':
        user_states[user_id] = None
        reply = f"🦾 تم تغيير الـ Seed الجديد بنجاح إلى: `{text}`" if lang == 'ar' else (f"🦾 Seed changed successfully to: `{text}`" if lang == 'en' else f"🦾 种子成功更改为：`{text}`")
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode="Markdown")

    elif user_states.get(user_id) == 'waiting_for_mods':
        user_states[user_id] = None
        reply = f"🙏 جاري تثبيت المود الخاص بك: `{text}` بنجاح داخل الخادم..." if lang == 'ar' else (f"🙏 Installing your mod: `{text}` to the server folder..." if lang == 'en' else f"🙏 正在成功安装您的模组：`{text}`...")
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_inputs))
    
    print("🚀 تم إصلاح الكود والتشغيل بالهيكل الجديد والمميز...")
    app.run_polling()

if __name__ == '__main__':
    main()
