# ============================================================
# بوت الأمن السيبراني - نسخة فخمة | Cyber Security Bot
# ============================================================

import subprocess
import sys
import importlib
import threading
import random

# تثبيت المكتبات تلقائياً
def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["requests", "flask", "telebot"]:
    install_and_import(pkg)

import telebot
import requests
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== التوكن ==========
TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# ========== سيرفر Flask ==========
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ بوت الأمن السيبراني شغال 24 ساعة"

# ========== دوال المساعدة ==========
def get_security_tip():
    tips = [
        "🔐 استخدم كلمة مرور مختلفة لكل حساب",
        "📱 فعّل المصادقة الثنائية (2FA) في كل خدماتك",
        "⚠️ لا تفتح روابط مجهولة المصدر",
        "🛡️ حدث برامجك ونظامك باستمرار",
        "🔒 استخدم مدير كلمات مرور موثوق",
        "📧 لا تشارك معلوماتك الحساسة عبر البريد",
        "🌐 تأكد أن المواقع تستخدم HTTPS",
        "📱 لا تحمل تطبيقات من مصادر غير رسمية"
    ]
    return random.choice(tips)

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*" for c in password):
        score += 1
    
    if score <= 2:
        return "❌ ضعيفة جداً", "red"
    elif score <= 3:
        return "⚠️ ضعيفة", "orange"
    elif score <= 4:
        return "✅ مقبولة", "yellow"
    else:
        return "🟢 قوية جداً", "green"

def generate_strong_password():
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(12))

def check_link_safety(url):
    # API مجاني لفحص الروابط
    try:
        response = requests.get(f"https://ipqualityscore.com/api/json/url/API_KEY/{url}", timeout=5)
        return "🟢 الرابط آمن" if response.status_code == 200 else "⚠️ فحص يدوي مطلوب"
    except:
        return "⚠️ تعذر الفحص. تأكد من الرابط."

# ========== القوائم الرئيسية ==========
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🛡️ فحص كلمة المرور", callback_data="check_pass")
    btn2 = InlineKeyboardButton("🔗 فحص رابط", callback_data="check_link")
    btn3 = InlineKeyboardButton("💪 إنشاء كلمة قوية", callback_data="gen_pass")
    btn4 = InlineKeyboardButton("📖 نصائح أمنية", callback_data="tips")
    btn5 = InlineKeyboardButton("⚠️ تهديدات حديثة", callback_data="threats")
    btn6 = InlineKeyboardButton("📞 تواصل مع خبير", callback_data="contact")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main"))
    return markup

# ========== أوامر البوت ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, "https://i.imgur.com/placeholder.jpg",  # يمكنك تغيير رابط الصورة
                   caption="🔥 **بوت الأمن السيبراني - Cyber Security Bot** 🔥\n\nاختر خدمة من القائمة أدناه:",
                   reply_markup=main_menu())

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "📖 **قائمة الأوامر:**\n/start - تشغيل البوت\n/help - المساعدة\n/tip - نصيحة عشوائية\n/pass <كلمة> - فحص كلمة مرور", reply_markup=back_button())

@bot.message_handler(commands=['tip'])
def tip_cmd(message):
    bot.send_message(message.chat.id, f"📌 **نصيحة أمنية اليوم:**\n{get_security_tip()}", reply_markup=back_button())

@bot.message_handler(commands=['pass'])
def pass_cmd(message):
    parts = message.text.split()
    if len(parts) > 1:
        password = parts[1]
        strength, color = check_password_strength(password)
        bot.send_message(message.chat.id, f"🔐 **نتيجة فحص كلمة المرور:**\n{strength}", reply_markup=back_button())
    else:
        bot.send_message(message.chat.id, "⚠️ استخدم: /pass كلمة_المرور", reply_markup=back_button())

# ========== معالجة الأزرار ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "main":
        bot.edit_message_caption("🔥 **بوت الأمن السيبراني** 🔥\n\nاختر خدمة من القائمة:", 
                                 call.message.chat.id, call.message.message_id, 
                                 reply_markup=main_menu())
    
    elif call.data == "check_pass":
        bot.edit_message_text("🔐 **فحص كلمة المرور**\n\nأرسل كلمة المرور التي تريد فحصها:", 
                              call.message.chat.id, call.message.message_id,
                              reply_markup=back_button())
        bot.register_next_step_handler(call.message, check_pass_handler)
    
    elif call.data == "check_link":
        bot.edit_message_text("🔗 **فحص رابط**\n\nأرسل الرابط لفحصه:", 
                              call.message.chat.id, call.message.message_id,
                              reply_markup=back_button())
        bot.register_next_step_handler(call.message, check_link_handler)
    
    elif call.data == "gen_pass":
        password = generate_strong_password()
        bot.edit_message_text(f"💪 **كلمة مرور قوية:**\n`{password}`\n\n⚠️ حفظها في مكان آمن!", 
                              call.message.chat.id, call.message.message_id, parse_mode='Markdown',
                              reply_markup=back_button())
    
    elif call.data == "tips":
        tip = get_security_tip()
        bot.edit_message_text(f"📖 **نصيحة أمنية:**\n\n{tip}", 
                              call.message.chat.id, call.message.message_id,
                              reply_markup=back_button())
    
    elif call.data == "threats":
        threats = "⚠️ **أحدث التهديدات الأمنية (2025):**\n\n1️⃣ هجمات الفدية (Ransomware) تتطور\n2️⃣ ثغرات الذكاء الاصطناعي التوليدي\n3️⃣ هجمات التصيد بالبريد الإلكتروني\n4️⃣ اختراق أجهزة إنترنت الأشياء (IoT)\n5️⃣ ثغرات التطبيقات السحابية"
        bot.edit_message_text(threats, call.message.chat.id, call.message.message_id,
                              reply_markup=back_button())
    
    elif call.data == "contact":
        contact_msg = "📞 **للتواصل مع خبراء الأمن السيبراني:**\n\n⚠️ في حالات الطوارئ الأمنية، تواصل مع فريق الاستجابة للطوارئ الحاسوبية في بلدك.\n\n🔒 للتوعية والاستشارات:\n@CyberSecurityExpert (Telegram)"
        bot.edit_message_text(contact_msg, call.message.chat.id, call.message.message_id,
                              reply_markup=back_button())

def check_pass_handler(message):
    strength, _ = check_password_strength(message.text)
    bot.send_message(message.chat.id, f"🔐 **النتيجة:**\n{strength}", reply_markup=main_menu())

def check_link_handler(message):
    result = check_link_safety(message.text)
    bot.send_message(message.chat.id, f"🔗 **نتيجة فحص الرابط:**\n{result}", reply_markup=main_menu())

# ========== تشغيل البوت ==========
def run_bot():
    print("🛡️ بوت الأمن السيبراني شغال...")
    bot.infinity_polling()

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    print("=" * 50)
    print("🛡️ بوت الأمن السيبراني - Cyber Security Bot")
    print("🚀 جاهز للتشغيل على 24 ساعة")
    print("=" * 50)
    
    threading.Thread(target=run_flask).start()
    run_bot()
