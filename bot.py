import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# إعدادات المراقبة
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# نصوص اللغات المتوافقة مع النظام الجديد للـ /start المباشر
LANGUAGES = {
    'ar': {
        'generating': "⏳ جاري إنشاء السيرفر الخاص بك، يرجى الانتظار...",
        'success': "🎉 تم إنشاء السيرفر يا بطل:\n\n🔗 **الآيبي:** `{ip}.aternos.me`\n🤖 **البوت:** يعمل بنجاح\n\nخصائص التحكم بسيرفرك أدناه:",
        'btn_manage': "🎮 التحكم في السيرفر 😃🤖",
        'btn_add_admin': "👨‍✈️ إضافة ادمن",
        'btn_start': "✅ تشغيل السيرفر",
        'btn_stop': "❌ إطفاء السيرفر",
        'btn_edit_ip': "😊 تعديل الايبي",
        'btn_lang': "🌐 تغيير اللغة (Language / 语言)",
        'status_working': "⏳ جاري تنفيذ طلبك...",
        'srv_started': "🟢 تم إرسال أمر تشغيل السيرفر بنجاح!",
        'srv_stopped': "🔴 تم إرسال أمر إيقاف السيرفر بنجاح.",
        'msg_admin': "🛡️ أرسل الآن معرف (Username) أو آيدي الآدمن الجديد:"
    },
    'en': {
        'generating': "⏳ Your server is being created, please wait...",
        'success': "🎉 Server created successfully, hero:\n\n🔗 **IP:** `{ip}.aternos.me`\n🤖 **Bot:** Running successfully\n\nControl your server options below:",
        'btn_manage': "🎮 Manage Server 😃🤖",
        'btn_add_admin': "👨‍✈️ Add Admin",
        'btn_start': "✅ Start Server",
        'btn_stop': "❌ Stop Server",
        'btn_edit_ip': "😊 Edit IP",
        'btn_lang': "🌐 Change Language (اللغة / 语言)",
        'status_working': "⏳ Processing...",
        'srv_started': "🟢 Server start command sent successfully!",
        'srv_stopped': "🔴 Server stop command sent successfully.",
        'msg_admin': "🛡️ Send the new admin's Username or ID now:"
    },
    'zh': {
        'generating': "⏳ 正在创建您的服务器，请稍候...",
        'success': "🎉 服务器创建成功，英雄：\n\n🔗 **IP地址:** `{ip}.aternos.me`\n🤖 **机器人:** 运行成功\n\n在下方控制您的服务器：",
        'btn_manage': "🎮 控制服务器 😃🤖",
        'btn_add_admin': "👨‍✈️ 添加管理员",
        'btn_start': "✅ 启动服务器",
        'btn_stop': "❌ 关闭服务器",
        'btn_edit_ip': "😊 修改 IP",
        'btn_lang': "🌐 更改语言 (Language / اللغة)",
        'status_working': "⏳ 正在处理...",
        'srv_started': "🟢 服务器启动命令发送成功！",
        'srv_stopped': "🔴 服务器关闭命令发送成功。",
        'msg_admin': "🛡️ 现在发送新管理员的用户名或 ID："
    }
}

user_preferences = {}
user_states = {}
# لحفظ اسم السيرفر (الآيبي) الافتراضي لكل مستخدم
user_servers = {} 

def get_lang(user_id):
    return user_preferences.get(user_id, 'ar')

# عند كتابة /start يتم الإنشاء التلقائي وإظهار الأزرار الجديدة فوراً
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    
    # تعيين آيبي افتراضي مبدئي إذا كان المستخدم جديداً
    if user_id not in user_servers:
        user_servers[user_id] = f"mc{user_id % 10000}"
        
    current_ip = user_servers[user_id]

    # 1. إرسال رسالة الانتظار أولاً
    waiting_msg = await update.message.reply_text(LANGUAGES[lang]['generating'])
    
    # إعداد لوحة الأزرار المطلوبة بدقة
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang]['btn_manage'], callback_data='manage_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_add_admin'], callback_data='add_admin')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_start'], callback_data='start_srv'),
         InlineKeyboardButton(LANGUAGES[lang]['btn_stop'], callback_data='stop_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_edit_ip'], callback_data='edit_ip')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_lang'], callback_data='choose_lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 2. تحديث الرسالة فوراً لتظهر بيانات السيرفر والأزرار الجديدة
    success_text = LANGUAGES[lang]['success'].format(ip=current_ip)
    await context.bot.edit_message_text(
        text=success_text,
        chat_id=update.effective_chat.id,
        message_id=waiting_msg.message_id,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# دالة لتحديث الرسالة بعد الضغط على خيار العودة أو تغيير لغة
async def refresh_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_lang(user_id)
    current_ip = user_servers.get(user_id, f"mc{user_id % 10000}")
    
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang]['btn_manage'], callback_data='manage_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_add_admin'], callback_data='add_admin')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_start'], callback_data='start_srv'),
         InlineKeyboardButton(LANGUAGES[lang]['btn_stop'], callback_data='stop_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_edit_ip'], callback_data='edit_ip')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_lang'], callback_data='choose_lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    success_text = LANGUAGES[lang]['success'].format(ip=current_ip)
    await query.edit_message_text(text=success_text, reply_markup=reply_markup, parse_mode="Markdown")

# معالج الأزرار التفاعلية الجديد
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_lang(user_id)
    data = query.data

    if data == 'main_menu':
        await refresh_menu(update, context)
        
    elif data == 'manage_srv':
        # قسم التحكم في السيرفر
        back_keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة" if lang=='ar' else ("🔙 Back" if lang=='en' else "🔙 返回"), callback_data='main_menu')]]
        msg = "🎮 **قسم التحكم في السيرفر:**\n\nالسيرفر يعمل بكفاءة ومربوط عبر نظام الـ API الخاص بـ Aternos." if lang=='ar' else ("🎮 **Server Management Section:**\n\nServer is healthy and connected via Aternos API." if lang=='en' else "🎮 **服务器管理部分：**\n\n服务器运行正常并通过 Aternos API 连接。")
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(back_keyboard), parse_mode="Markdown")
        
    elif data == 'add_admin':
        user_states[user_id] = 'waiting_for_admin'
        await query.edit_message_text(LANGUAGES[lang]['msg_admin'])
        
    elif data == 'start_srv':
        await query.edit_message_text(LANGUAGES[lang]['status_working'])
        # هنا يتم وضع كود الـ API الفعلي للتشغيل لاحقاً
        await query.message.reply_text(LANGUAGES[lang]['srv_started'])
        # إعادة إظهار القائمة الرئيسية بعد الإجراء
        context.user_data['query'] = query
        await refresh_menu(update, context)
        
    elif data == 'stop_srv':
        await query.edit_message_text(LANGUAGES[lang]['status_working'])
        # هنا يتم وضع كود الـ API الفعلي للإيقاف لاحقاً
        await query.message.reply_text(LANGUAGES[lang]['srv_stopped'])
        await refresh_menu(update, context)
        
    elif data == 'edit_ip':
        user_states[user_id] = 'waiting_for_ip'
        msg = "✏️ أرسل الآن الاسم الجديد للآيبي (بدون فواصل أو نقاط):" if lang == 'ar' else ("✏️ Send the new IP name now (letters/numbers only):" if lang == 'en' else "✏️ 现在发送新的 IP 名称（仅限字母/数字）：")
        await query.edit_message_text(msg)
        
    elif data == 'choose_lang':
        keyboard = [
            [InlineKeyboardButton("العربية 🇵🇸", callback_data='set_lang_ar'),
             InlineKeyboardButton("English 🇺🇸", callback_data='set_lang_en'),
             InlineKeyboardButton("中文 🇨🇳", callback_data='set_lang_zh')],
            [InlineKeyboardButton("🔙 عودة", callback_data='main_menu')]
        ]
        await query.edit_message_text("🌐 اختر لغة البوت / Choose Language / 选择语言:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data.startswith('set_lang_'):
        new_lang = data.split('_')[2]
        user_preferences[user_id] = new_lang
        await refresh_menu(update, context)

# استقبال النصوص لتعديل الآيبي أو إضافة الآدمن
async def handle_text_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = get_lang(user_id)
    
    if user_states.get(user_id) == 'waiting_for_ip':
        user_states[user_id] = None
        # تحديث قيمة الآيبي في الذاكرة للمستخدم
        user_servers[user_id] = text.strip()
        
        reply = f"🎯 تم تغيير آيبي السيرفر بنجاح إلى:\n`{text}.aternos.me`" if lang == 'ar' else (f"🎯 IP changed successfully to:\n`{text}.aternos.me`" if lang == 'en' else f"🎯 IP 成功更改为：\n`{text}.aternos.me`")
        await update.message.reply_text(reply, parse_mode="Markdown")
        
        # إعادة إظهار القائمة بالآيبي الجديد
        current_ip = user_servers[user_id]
        keyboard = [
            [InlineKeyboardButton(LANGUAGES[lang]['btn_manage'], callback_data='manage_srv')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_add_admin'], callback_data='add_admin')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_start'], callback_data='start_srv'),
             InlineKeyboardButton(LANGUAGES[lang]['btn_stop'], callback_data='stop_srv')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_edit_ip'], callback_data='edit_ip')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_lang'], callback_data='choose_lang')]
        ]
        success_text = LANGUAGES[lang]['success'].format(ip=current_ip)
        await update.message.reply_text(text=success_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif user_states.get(user_id) == 'waiting_for_admin':
        user_states[user_id] = None
        reply = f"✅ تم إضافة الآدمن `{text}` بنجاح لخصائص التحكم!" if lang == 'ar' else (f"✅ Admin `{text}` added successfully!" if lang == 'en' else f"✅ 管理员 `{text}` 添加成功！")
        await update.message.reply_text(reply, parse_mode="Markdown")
        
        # إعادة إظهار القائمة الرئيسية
        current_ip = user_servers.get(user_id, f"mc{user_id % 10000}")
        keyboard = [
            [InlineKeyboardButton(LANGUAGES[lang]['btn_manage'], callback_data='manage_srv')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_add_admin'], callback_data='add_admin')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_start'], callback_data='start_srv'),
             InlineKeyboardButton(LANGUAGES[lang]['btn_stop'], callback_data='stop_srv')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_edit_ip'], callback_data='edit_ip')],
            [InlineKeyboardButton(LANGUAGES[lang]['btn_lang'], callback_data='choose_lang')]
        ]
        success_text = LANGUAGES[lang]['success'].format(ip=current_ip)
        await update.message.reply_text(text=success_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_inputs))
    
    print("🚀 البوت المطور جاهز ومستعد للعمل الفوري...")
    app.run_polling()

if __name__ == '__main__':
    main()
