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
        'lang_success': "تم تغيير لغة البوت إلى العربية بنجاح! 🇵🇸",
        'control_panel': "🎛️ لوحة التحكم بالسيرفر - اختر الإجراء أو الإعداد لتعديله:",
        'btn_start': "🟢 تشغيل السيرفر",
        'btn_stop': "🔴 إيقاف السيرفر",
        'btn_restart': "🔄 إعادة تشغيل",
        'btn_seed': "🌱 تغيير الـ Seed (عالم جديد)",
        'btn_slots': "👥 عدد اللاعبين المسموح",
        'btn_op': "👑 إضافة أدمن للسيرفر (OP)",
        'btn_back': "🔙 العودة للقائمة الرئيسية",
        'btn_create_bedrock': "📱 إنشاء سيرفر Bedrock (جوال)",
        'btn_create_java': "💻 إنشاء سيرفر Java (كمبيوتر)",
        'sending': "⏳ جاري تنفيذ الطلب وإرسال الإشارة المباشرة...",
        'no_permission': "❌ عذراً! هذا الخيار مخصص للأدمن قُصي فقط."
    },
    'en': {
        'welcome': "🚀 Welcome Qusai to the advanced Minecraft Server control panel!",
        'btn_servers': "📂 My Servers",
        'btn_control': "🎮 Server Control Panel",
