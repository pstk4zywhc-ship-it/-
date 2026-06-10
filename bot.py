import os
import telebot
import urllib.parse
import requests  # مكتبة جديدة لتحميل الصور بأمان

# توكن التلغرام الخاص بك
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

    waiting_message = bot.reply_to(message, f"🔄 جاري تصميم وتوليد السكن الخاص بك... قد يستغرق الأمر من 5 إلى 10 ثوانٍ.")

    # تحديد مسار ملف الصورة المؤقتة بناءً على آيدي المستخدم
    temp_image_path = f"skin_{message.chat.id}.png"

    try:
        # تحسين الوصف ليتناسب مع محرك الصور المجاني ليعطي شكل سكن ماينكرافت
        enhanced_prompt = (
            f"Minecraft character skin, full body 3D render pose and flat texture layout template next to it, "
            f"{user_description}, pixel art style, 16-bit, game asset"
        )
        
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=55&model=flux"

        # الخطوة السحرية: البوت يقوم بتحميل الصورة أولاً وينتظر السيرفر حتى ينتهي
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200:
            # حفظ الصورة مؤقتاً على السيرفر
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
            
            # إرسال الصورة المحفوظة كملف حقيقي للتفادي خطأ التلغرام
            with open(temp_image_path, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🎁 تفضل! هذا هو السكن الخاص بك بناءً على وصفك: `{user_description}`.",
                    parse_mode='Markdown'
                )
        else:
            bot.reply_to(message, "⚠️ عذراً، سيرفر توليد الصور مشغول حالياً، يرجى المحاولة مرة أخرى بعد قليل.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء التوليد: {str(e)}")
    finally:
        # حذف رسالة الانتظار
        bot.delete_message(message.chat.id, waiting_message.message_id)
        # تنظيف وحذف ملف الصورة المؤقتة من السيرفر
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

# تشغيل البوت
bot.infinity_polling()
