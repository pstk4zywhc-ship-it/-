import os
import telebot
import urllib.parse
import requests
from flask import Flask
from threading import Thread

# توكن التلغرام الخاص بك
TELEGRAM_BOT_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Minecraft Skin Bot is Running!"

def run_web_server():
    # Railway يحدد المنفذ تلقائياً عبر متغير البيئة PORT، وإذا لم يجده يستخدم 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# 🎯 الدالة السحرية لتوليد رابط سكن ماينكرافت (وليس صورة عادية)
def get_minecraft_skin_url(description):
    # تحويل الوصف إلى الإنجليزية وتحديد شكل سكن ماينكرافت المقصوص
    prompt = f"Minecraft player skin, unfolded template layout and standing 3D preview, pixel art 16x16, accurate design of: {description}"
    encoded_prompt = urllib.parse.quote(prompt)
    
    # استخدام رابط توليد عالي الجودة ومستقر
    return f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=99"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 *أهلاً بك في بوت سكنات ماينكرافت النهائي 24/7!* 🤖\n\n"
        "اكتب لي وصفاً للسكن الذي تريده (مثلاً: `black ninja with red eyes` أو `golden warrior`)، "
        "وسأقوم بتوليد صورة تعرض لك شكل السكن ثلاثي الأبعاد ومعها خريطة التصميم (Skin map) الجاهزة!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_skin_description(message):
    user_description = message.text

    if len(user_description) < 3:
        bot.reply_to(message, "يرجى كتابة وصف أطول وأكثر وضوحاً للسكن.")
        return

    waiting_message = bot.reply_to(message, f"🔄 جاري الاتصال بمحرك الرسوم الذكي لتصميم سكنك... انتظر لحظات.")

    temp_image_path = f"skin_{message.chat.id}.png"

    try:
        # جلب رابط صورة السكن بدقة
        image_url = get_minecraft_skin_url(user_description)
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
            
            with open(temp_image_path, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🎁 تفضل السكن الكامل والمعاينة لوصفك: `{user_description}`\n\nتحتوي الصورة على الشكل ثلاثي الأبعاد وخريطة السكن الجاهزة للتطبيق!",
                    parse_mode='Markdown'
                )
        else:
            raise Exception("سيرفر التوليد لم يستجب بشكل صحيح.")

    except Exception as e:
        bot.reply_to(message, "⚠️ عذراً، محرك الصور مشغول حالياً. يرجى المحاولة مرة أخرى بعد دقيقة.")

    finally:
        if bot and waiting_message:
            try:
                bot.delete_message(message.chat.id, waiting_message.message_id)
            except:
                pass
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

# تشغيل البوت وخادم الويب معاً
if __name__ == "__main__":
    keep_alive()  # تشغيل سيرفر الويب في الخلفية لـ UptimeRobot
    bot.infinity_polling()  # تشغيل البوت لاستقبال الرسائل
