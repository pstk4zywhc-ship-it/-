import os
import telebot
import urllib.parse

# ضع توكن التلغرام الخاص بك هنا
TELEGRAM_BOT_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 *أهلاً بك في بوت سكنات ماينكرافت المجاني!* 🤖\n\n"
        "اكتب لي وصفاً للسكن الذي تريده (باللغة الإنجليزية لأفضل نتائج)، "
        "وسأقوم بتوليد صورة تعرض لك شكل السكن ثلاثي الأبعاد ومعها خريطة التصميم مجاناً!\n\n"
        "مثال: `Minecraft skin of a cool neon blue ninja`"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_skin_description(message):
    user_description = message.text

    if len(user_description) < 3:
        bot.reply_to(message, "يرجى كتابة وصف أطول وأكثر وضوحاً للسكن.")
        return

    waiting_message = bot.reply_to(message, f"🔄 جاري تصميم سكن ماينكرافت الخاص بك... انتظر ثواني قليلة.")

    try:
        # تحسين الوصف ليفهمه محرك الصور المجاني ويصنع سكن ماينكرافت
        enhanced_prompt = (
            f"Minecraft character skin, full body 3D render pose and flat texture layout template next to it, "
            f"{user_description}, pixel art style, 16-bit, game asset"
        )
        
        # تحويل النص ليكون متوافقاً مع الروابط (URL Encoding)
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # استخدام رابط التوليد المجاني المباشر (يعتمد على ذكاء اصطناعي مفتوح المصدر)
        image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"

        # إرسال الصورة الناتجة للمستخدم فوراً
        bot.send_photo(
            message.chat.id,
            image_url,
            caption=f"🎁 تفضل! هذا هو السكن الخاص بك بناءً على وصفك: `{user_description}`.",
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.reply_to(message, f"⚠️ عذراً، حدث خطأ أثناء التوليد: {str(e)}")
    finally:
        # حذف رسالة الانتظار
        bot.delete_message(message.chat.id, waiting_message.message_id)

# تشغيل البوت
bot.infinity_polling()
