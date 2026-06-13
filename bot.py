# ============================================================
# بوت تلجرام - نسخة شاملة ذاتية التثبيت (تعمل على أي منصة)
# ============================================================

import subprocess
import sys
import importlib
import threading

# 🔧 1. تثبيت المكتبات تلقائياً (أول مرة فقط)
def install_and_import(package):
    try:
        importlib.import_module(package)
        print(f"✅ {package} مثبت مسبقاً")
    except ImportError:
        print(f"📦 جاري تثبيت {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} تم تثبيته")

# المكتبات المطلوبة
required_packages = ["requests", "flask", "telebot"]
for package in required_packages:
    install_and_import(package)

# استيراد المكتبات
import telebot
import requests
from flask import Flask

# ============================================================
# 🔑 توكن البوت (تم وضعه بأمرك)
# ============================================================
TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# ============================================================
# 🌐 سيرفر Flask (لإرضاء منصات الاستضافة)
# ============================================================
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة!"

@flask_app.route('/health')
def health():
    return "OK"

# ============================================================
# 🧠 الذكاء الاصطناعي (مجاني 100%)
# ============================================================
def get_ai_reply(question):
    try:
        response = requests.get(f"https://hercai.onrender.com/v3/hercai?question={question}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("reply", "آسف، ما فهمتك.")
        return "⚠️ عطل مؤقت في الذكاء. حاول مرة ثانية."
    except Exception as e:
        return f"🔌 خطأ في الاتصال: {str(e)[:50]}"

# ============================================================
# 📋 أوامر البوت
# ============================================================
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🤖 **مرحباً! أنا بوت ذكي شغال 24 ساعة**\n\nأرسل أي شيء وسأرد عليك بالذكاء الاصطناعي.\n/help للمساعدة")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "📖 **الأوامر المتاحة:**\n/start - بدء البوت\n/help - هذه المساعدة\n/reset - مسح المحادثة\n\n💬 فقط اكتب أي شيء وسأجيبك.")

@bot.message_handler(commands=['reset'])
def reset_command(message):
    bot.reply_to(message, "🗑️ تم مسح تاريخ المحادثة. ابدأ من جديد.")

# ============================================================
# 💬 الرد على جميع الرسائل
# ============================================================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = get_ai_reply(message.text)
    bot.reply_to(message, reply)

# ============================================================
# 🚀 تشغيل البوت والسيرفر معاً
# ============================================================
def run_bot():
    print("🤖 جاري تشغيل البوت...")
    bot.infinity_polling()

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 بوت تلجرام - جاهز للتشغيل")
    print(f"🔑 التوكن المستخدم: {TOKEN[:15]}...")
    print("=" * 50)
    
    # تشغيل البوت في خلفية
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # تشغيل سيرفر Flask
    run_flask()
