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
        # تحسين البرومبت بالإنجليزية ليعطي تفاصيل أدق
        enhanced_prompt = (
            f"Minecraft character skin texture, 3D render, {user_description}, pixel art style"
        )
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # استخدام خادم دمج عالي الاستقرار وسريع جداً مع Railway
        image_url = f"https://api.v0.models.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=100"

        # محاولة جلب الصورة مع زيادة وقت الانتظار وتخطي الحظر عبر إضافة Headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(image_url, headers=headers, timeout=40)
        
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
            # إذا فشل السيرفر الأول، سنستخدم سيرفر احتياطي فوري وسريع جداً لكي لا يقف البوت
            fallback_url = f"https://robohash.org/{encoded_prompt}.png?set=set4"
            fallback_res = requests.get(fallback_url, timeout=20)
            
            with open(temp_image_path, 'wb') as f:
                f.write(fallback_res.content)
                
            with open(temp_image_path, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🎁 السيرفر الرئيسي مضغوط، تفضل هذا التصميم البديل السريع لوصفك: `{user_description}`",
                    parse_mode='Markdown'
                )

    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء التوليد: {str(e)}")
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
