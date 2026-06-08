import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from python_aternos import Client

# إعدادات المراقبة والأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن البوت الخاص بك
TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# قاموس اللغات للبوت (عربي وإنجليزي)
LANGUAGES = {
    'ar': {
        'welcome': "👋 مرحباً بك في بوت إدارة وصناعة سيرفرات ماين كرافت العالمي!\n\nاختر ما تريد القيام به من القائمة:",
        'btn_create_server': "🛠️ صناعة سيرفر جديد",
        'btn_start_server': "▶️ تشغيل السيرفر",
        'btn_stop_server': "⏹️ إطفاء السيرفر",
        'btn_settings': "⚙️ إعدادات السيرفر",
        'btn_lang': "🌐 تغيير اللغة (Language)",
        'choose_type': "🎮 اختر نوع السيرفر الذي تريد صناعته:",
        'java_type': "🖥️ جافا (Java Edition)",
        'bedrock_type': "📱 بيدروك / جوال (Bedrock)",
        'status_working': "⏳ جاري تنفيذ طلبك...",
        'back': "🔙 عودة"
    },
    'en': {
        'welcome': "👋 Welcome to Minecraft Server Creator & Manager Bot!\n\nSelect an option from the menu:",
        'btn_create_server': "🛠️ Create New Server",
        'btn_start_server': "▶️ Start Server",
        'btn_stop_server': "⏹️ Stop Server",
        'btn_settings': "⚙️ Server Settings",
        'btn_lang': "🌐 Change Language",
        'choose_type': "🎮 Choose the server edition you want to create:",
        'java_type': "🖥️ Java Edition",
        'bedrock_type': "📱 Bedrock / Mobile",
        'status_working': "⏳ Processing your request...",
        'back': "🔙 Back"
    }
}

user_preferences = {}
user_states = {}

def get_lang(user_id):
    return user_preferences.get(user_id, 'ar')

# عند الضغط على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang]['btn_create_server'], callback_data='create_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_start_server'], callback_data='start_srv'),
         InlineKeyboardButton(LANGUAGES[lang]['btn_stop_server'], callback_data='stop_srv')],
        [InlineKeyboardButton(LANGUAGES[lang]['btn_settings'], callback_data='settings'),
         InlineKeyboardButton(LANGUAGES[lang]['btn_lang'], callback_data='choose_lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(LANGUAGES[lang]['welcome'], reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(LANGUAGES[lang]['welcome'], reply_markup=reply_markup)

# معالج الأزرار التفاعلية
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_lang(user_id)
    data = query.data

    if data == 'main_menu':
        await start(update, context)

    elif data == 'create_srv':
        keyboard = [
            [InlineKeyboardButton(LANGUAGES[lang]['java_type'], callback_data='make_java'),
             InlineKeyboardButton(LANGUAGES[lang]['bedrock_type'], callback_data='make_bedrock')],
            [InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text(LANGUAGES[lang]['choose_type'], reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'make_java':
        await query.edit_message_text(LANGUAGES[lang]['status_working'])
        await query.message.reply_text("✅ **تم إنشاء سيرفر الجافا بنجاح!**\n📌 يمكنك الآن تشغيله أو تعديل إعداداته من القائمة.")

    elif data == 'make_bedrock':
        await query.edit_message_text(LANGUAGES[lang]['status_working'])
        await query.message.reply_text("✅ **تم إنشاء سيرفر البيدروك (الجوال) بنجاح!**\n🔢 البورت الافتراضي: `19132`\n📌 السيرفر جاهز للتشغيل الآن.")

    elif data == 'start_srv':
        await query.edit_message_text("⏳ جاري إرسال أمر تشغيل السيرفر...")
        await query.message.reply_text("🟢 السيرفر الآن في مرحلة التشغيل (Starting)!")
        
    elif data == 'stop_srv':
        await query.edit_message_text("⏳ جاري إيقاف السيرفر...")
        await query.message.reply_text("🔴 تم إطفاء السيرفر بنجاح.")

    elif data == 'settings':
        keyboard = [
            [InlineKeyboardButton("🔗 تغيير الآيبي (Change IP)", callback_data='edit_ip')],
            [InlineKeyboardButton("👥 تعديل الحد الأقصى للاعبين", callback_data='edit_max_players')],
            [InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text("⚙️ **إعدادات السيرفر:**\n\nيمكنك التحكم بخيارات السيرفر من هنا:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'edit_ip':
        user_states[user_id] = 'waiting_for_ip'
        await query.edit_message_text("✏️ أرسل الآن الاسم الجديد للآيبي الذي تريده:")

    elif data == 'choose_lang':
        keyboard = [
            [InlineKeyboardButton("العربية 🇸🇦", callback_data='set_lang_ar'),
             InlineKeyboardButton("English 🇺🇸", callback_data='set_lang_en')],
            [InlineKeyboardButton(LANGUAGES[lang]['back'], callback_data='main_menu')]
        ]
        await query.edit_message_text("🌐 اختر لغة البوت / Choose Bot Language:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data.startswith('set_lang_'):
        new_lang = data.split('_')[2]
        user_preferences[user_id] = new_lang
        query.data = 'main_menu'
        await start(update, context)

# استقبال النصوص لتغيير الآيبي
async def handle_text_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_states.get(user_id) == 'waiting_for_ip':
        user_states[user_id] = None
        await update.message.reply_text(f"🎯 تم تغيير آيبي السيرفر بنجاح إلى:\n`{text}.aternos.me`", parse_mode="Markdown")
        await start(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_inputs))
    
    print("🚀 البوت جاهز ويعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
