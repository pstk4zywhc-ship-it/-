import telebot
from telebot import types
import requests
import time

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ADMIN_USERNAME = "sssss111126"

# قاموس اللغات المتكامل
LANGUAGES = {
    'ar': {
        'welcome': "🚀 أهلاً بك يا قُصي في لوحة تحكم أترنوس المحدثة بالكامل!",
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
        'sending': "⏳ جاري إرسال الإشارة الرسمية وتأمين الاتصال السريع...",
        'success_start': "✅ **تم إرسال أمر التشغيل المباشر بنجاح وتخطي الحماية!**\n\nالسيرفر يقلع الآن، انتظر دقيقة ثم ادخل اللعبة مباشرة.\n🌐 **الـ IP:** `{user}.aternos.me`\n🔌 **الـ Port:** `19132`",
        'success_stop': "🛑 تم إرسال أمر إيقاف السيرفر بنجاح.",
        'success_restart': "🔄 جاري إعادة تشغيل السيرفر الآن، انتظر قليلاً.",
        'success_delete': "🗑️ تم إرسال أمر الحذف وتطهير الحساب.",
        'no_permission': "❌ هذا الخيار مخصص للأدمن قُصي فقط!"
    },
    'en': {
        'welcome': "🚀 Welcome Qusai to the updated Aternos control panel!",
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
        'sending': "⏳ Sending bypass signal to Aternos...",
        'success_start': "✅ **Server Started Successfully!**\n\n🌐 **IP:** `{user}.aternos.me`\n🔌 **Port:** `19132`",
        'success_stop': "🛑 Server stopped successfully.",
        'success_restart': "🔄 Restarting the server now...",
        'success_delete': "🗑️ Delete command sent successfully.",
        'no_permission': "❌ This command is for Admin Qusai only!"
    },
    'zh': {
        'welcome': "🚀 欢迎 Qusai 使用更新的 Aternos 控制面板！",
        'btn_servers': "📂 我的服务器",
        'btn_control': "🎮 服务器控制面板",
        'btn_lang': "🌐 更改语言",
        'btn_admin': "🔒 管理员列表",
        'choose_lang':
 