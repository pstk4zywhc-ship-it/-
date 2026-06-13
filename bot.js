import telebot
import requests
import time
import threading
from flask import Flask, request

# ========== توكن البوت ==========
TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# ========== سيرفر Flask عشان Render ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة!", 200

@app.route('/health')
def health():
    return "OK", 200

# ========== الذكاء الاصطناعي (مجاني) ==========
def get_ai_reply(question):
    try:
        response = requests.get(f"https://hercai.onrender.com/v3/hercai?question={question}", timeout=15)
        if response.status_code == 200:
            return response.json().get("reply", "آسف، ما فهمتك.")
        return "⚠️ عطل مؤقت في الذكاء"
    except:
        return "🔌 خطأ في الاتصال"

# ========== أوامر البوت ==========
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🤖 مرحباً! أنا بوت ذكي شغال 24 ساعة.\nأرسل أي شيء وسأرد عليك.")

@bot.message_handler(commands=['help'])
def help(m):
    bot.reply_to(m, "📖 أرسل أي نص أو سؤال وسأرد عليك بالذكاء الاصطناعي.")

@bot.message_handler(commands=['reset'])
def reset(m):
    bot.reply_to(m, "🗑️ تم مسح المحادثة.")

@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.send_chat_action(m.chat.id, 'typing')
    reply = get_ai_reply(m.text)
    bot.reply_to(m, reply)

# ========== تشغيل البوت والسيرفر معاً ==========
def run_bot():
    print("🤖 البوت شغال...")
    bot.infinity_polling()

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_bot).start()
    print("✅ تم تشغيل البوت وسيرفر الصحة")
