import os
import telebot
from openai import OpenAI

# 1. إعداد المفاتيح (تم دمج توكن التلغرام الخاص بك هنا)
TELEGRAM_BOT_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
OPENAI_API_KEY = "ضع_مفتاح_API_من_OPENAI_هنا"  # استبدل هذا بمفتاح OpenAI الخاص بك

# 2. تهيئة العملاء
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# نتحقق أولاً إذا قمت بوضع مفتاح OpenAI لتجنب توقف البوت
if OPENAI_API_KEY != "ضع_مفتاح_API_من_OPENAI_هنا":
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

def generate_minecraft_skin(description):
    """دالة لتوليد السكن وصورة الأنسجة باستخدام DALL-E 3"""
    if not client:
        return "error_key"
        
    full_prompt = (
        f"A detailed digital art image of a unique Minecraft character skin based on the following description: {description}. "
        f"The image must show two things clearly separated: "
        f"1. A full-body 3D render of the character in a cool pose. "
        f"2. A flat, unfolding texture map layout (skin template) of the same character next to it, which looks like a real Minecraft skin file ready to be used. "
        f"The style must be blocky, pixelated, 16-bit Minecraft pixel art."
    )

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 *أهلاً بك في بوت صانع سكنات ماينكرافت الذكي!* 🤖\n\n"
        "اكتب لي وصفاً للسكن الذي تريده (مثلاً: نينجا أسود بعيون حمراء، أو محارب ذهبي)، "
        "وسأقوم بتوليد صورة تعرض لك شكل السكن ثلاثي الأبعاد ومعها خريطة الأنسجة الخاصة به!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_skin_description(message):
    user_description = message.text

    if len(user_description) < 3:
        bot.reply_to(message, "يرجى كتابة وصف أطول وأكثر وضوحاً للسكن لتكون النتيجة ممتازة.")
        return

    waiting_message = bot.reply_to(message, f"🔄 جاري تصميم سكن ماينكرافت الخاص بك بناءً على وصفك... قد يستغرق هذا حوالي 30 ثانية.")

    # توليد الصورة
    image_url = generate_minecraft_skin(user_description)

    # حذف رسالة الانتظار
    bot.delete_message(message.chat.id, waiting_message.message_id)

    if image_url == "error_key":
        bot.reply_to(message, "⚠️ خطأ: لم يتم إعداد `OPENAI_API_KEY` داخل الكود بشكل صحيح. يرجى تزويد البوت بالمفتاح أولاً.")
    elif image_url:
        bot.send_photo(
            message.chat.id,
            image_url,
            caption=f"🎁 تفضل! هذا هو السكن الخاص بك بناءً على وصفك: `{user_description}`.\n\nتحتوي الصورة على الشكل النهائي وخريطة التصميم المقصوصة.",
            parse_mode='Markdown'
        )
    else:
        bot.reply_to(message, "⚠️ عذراً، واجه الذكاء الاصطناعي مشكلة في فهم أو توليد هذا الوصف، حاول مجدداً بوصف آخر.")

# تشغيل البوت
bot.infinity_polling()
