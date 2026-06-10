import os
import telebot
import urllib.parse
import requests

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

    waiting_message = bot.reply_to(message, f"🔄 جاري الاتصال بمحرك الرسوم الذكي لتصميم سكنك... انتظر لحظات.")

    temp_image_path = f"skin_{message.chat.id}.png"

    try:
        # تحسين البرومبت ليفهمه الذكاء الاصطناعي بشكل أفضل
        enhanced_prompt = (
            f"Minecraft character skin, 3D full body render pose, pixel art style, {user_description}"
        )
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # استخدام رابط توليد مباشر ومستقر جداً وبديل مجاني
        image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true"

        # إرسال طلب جلب الصورة مع خيار عدم إطالة الانتظار
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(image_url, headers=headers, timeout=25)
        
        if response.status_code == 200:
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
            
            with open(temp_image_path, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🎁 تفضل السكن الخاص بك بناءً على وصفك: `{user_description}`\n\nقم بحفظ الصورة وتطبيقها داخل ماينكرافت!",
                    parse_mode='Markdown'
                )
        else:
            raise Exception("سيرفر التوليد لم يستجب بشكل صحيح.")

    except Exception as e:
        # خطة بديلة فورية ومضمونة 100% في حال فشل الاتصال بالذكاء الاصطناعي لتوليد الـ Skin
        try:
            fallback_url = f"https://robohash.org/{encoded_prompt}.png?set=set4"
            fallback_res = requests.get(fallback_url, timeout=15)
            
            with open(temp_image_path, 'wb') as f:
                f.write(fallback_res.content)
                
            with open(temp_image_path, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🎁 تفضل هذا التصميم السريع لوصفك: `{user_description}`\n*(السيرفر الرئيسي مضغوط حالياً)*",
                    parse_mode='Markdown'
                )
        except Exception as fallback_error:
            bot.reply_to(message, "⚠️ عذراً، هناك ضغط كبير على سيرفرات الصور حالياً. يرجى المحاولة مرة أخرى بعد دقيقة.")

    finally:
        if bot:
            try:
                bot.delete_message(message.chat.id, waiting_message.message_id)
            except:
                pass
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

# تشغيل البوت
bot.infinity_polling()
