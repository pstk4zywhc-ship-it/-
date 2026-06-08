import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# إعدادات المراقبة
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# قاموس اللغات المتوافق تماماً مع الهيكل الجديد
LANGUAGES = {
    'ar': {
        'welcome': "👋 مرحباً بك في بوت إدارة وصناعة سيرفرات ماين كرافت العالمي!\n\nاختر ما تريد القيام به من القائمة أدناه:",
        'btn_create_server': "انشاء سيرفر 👾",
        'btn_manage': "التحكم في السيرفر👨‍✈️",
        'btn_edit_ip': "تعديل الآي بي💯",
        'btn_add_mods': "اضافة مودات للسيرفر 🙏",
        'btn_change_seed': "تغيير الseed 🦾",
        'btn_start': "تشغيل السيرفر ✅",
        'btn_stop': "إطفاء السيرفر ❌",
        'btn_lang': "🌐 تغيير اللغة (Language / 语言)",
        'choose_type': "🎮 اختر نوع السيرفر الذي تريد صناعته:",
        'java_type': "🖥️ جافا (Java Edition)",
        'bedrock_type': "📱 بيدروك / جوال (Bedrock)",
        'status_working': "⏳ جاري تنفيذ طلبك، يرجى الانتظار...",
        'success_msg': "🎉 تم إنشاء السيرفر بنجاح يا بطل!\n\n🔗 **الآيبي:** `{ip}.aternos.me`\n🤖 **البوت:** يعمل وجاهز للتحكم.",
        'msg_ip': "✏️ أرسل الآن الاسم الجديد للآيبي (بدون فواصل أو نقاط):",
        'msg_seed': "✏️ أرسل الـ Seed الجديد الذي تريد تعيينه للعالم:",
        'msg_mods': "📦 أرسل اسم المود أو الملف الذي تريد إضافته للسيرفر:",
        'back': "🔙 عودة للرئيسية"
    },
    'en': {
        'welcome': "👋 Welcome to the Minecraft Server Manager Bot!\n\nSelect an option from the menu:",
        'btn_create_server': "Create Server 👾",
        'btn_manage': "Manage Server 👨‍✈️",
        'btn_edit_ip': "Edit IP 💯",
        'btn_add_mods': "Add Mods to Server 🙏",
        'btn_change_seed': "Change Seed 🦾",
        'btn_start': "Start Server ✅",
        'btn_stop': "Stop Server ❌",
        'btn_lang': "🌐 Change Language (اللغة / 语言)",
        'choose_type': "🎮 Choose server edition:",
        'java_type': "🖥️ Java Edition",
        'bedrock_type': "📱 Bedrock / Mobile",
        'status_working': "⏳ Processing, please wait...",
        'success_msg': "🎉 Server created successfully, hero!\n\n🔗 **IP:** `{ip}.aternos.me`\n🤖 **Bot:** Active and ready.",
        'msg_ip': "✏️ Send the new IP name (letters/numbers only):",
        'msg_seed': "✏️ Send the new Seed you want to set for the world:",
        'msg_mods': "📦 Send the name or file of the mod you want to add:",
        'back': "🔙 Back to Menu"
    },
    'zh': {
        'welcome': "👋 欢迎使用我的世界服务器
