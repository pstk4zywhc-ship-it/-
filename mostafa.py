import telebot
import requests
import threading
from flask import Flask

# ========== توكن البوت ==========
TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN)

# ========== سيرفر Flask ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة!"

@app.route('/health')
def health():
    return "OK"

# ========== الذكاء الاصطناعي ==========
def get_ai_reply(question):
    try:
        response = requests.get(f"https://hercai.onrender.com/v3/hercai?question={question}", timeout=15)
        if response.status_code == 200:
            return response.json().get("reply", "آسف، ما فهمتك.")
        return "⚠️ عطل مؤقت"
    except:
        return "🔌 خطأ في الاتصال"

# ========== أوامر البوت ==========
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🤖 مرحباً! أنا بوت mostafa الذكي")

@bot.message_handler(commands=['help'])
def help(m):
    bot.reply_to(m, "أرسل أي شيء وسأرد عليك.")

@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.send_chat_action(m.chat.id, 'typing')
    reply = get_ai_reply(m.text)
    bot.reply_to(m, reply)

# ========== التشغيل ==========
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8080)
