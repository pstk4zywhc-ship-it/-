import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# جلب التوكن من إعدادات المنصة أو استخدام التوكن الخاص بك مباشرة
TOKEN = os.getenv("TELEGRAM_TOKEN", "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM")

# قاعدة بيانات المسلسلات المحدثة
EGYPTIAN_SERIES = {
    "الأسطورة": {
        "story": "تدور أحداث المسلسل حول ناصر، شاب خريج كلية الحقوق يسعى للانضمام للسلك القضائي، ولكن بسبب الظروف الاجتماعية وشقيقه رفاعي يتغير مسار حياته تماماً ويدخل في عالم تجارة السلاح والدراما المشوقة.",
        "video_id": "https://t.me/c/123456789/4"  # ضع هنا رابط قناة التليجرام أو ملف الحلقات لمسلسل الأسطورة
    },
    "جعفر العمدة": {
        "story": "تدور الأحداث في إطار اجتماعي شعبي حول جعفر العمدة الذي يعيش في حي السيدة زينب ويمتلك شركات للمقاولات ويبحث عن ابنه المفقود منذ سنوات.",
        "video_id": "https://t.me/c/123456789/1"
    },
    "الاختيار": {
        "story": "يتناول العمل بطولات رجال القوات المسلحة والشرطة المصرية والتضحيات التي يقدمونها لحماية الوطن.",
        "video_id": "https://t.me/c/123456789/2"
    },
    "الكبير أوي": {
        "story": "مغامرات كوميدية في قرية المزاريطة بين الكبير وجوني وحزلقوم ومواقفهم الطريفة مع أهل القرية.",
        "video_id": "https://t.me/c/123456789/3"
    }
}

# أمر /start عند تشغيل البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    welcome_text = (
        f"أهلاً بك يا {user_name} في بوت المسلسلات المصرية! 🎬\n\n"
        "اكتب اسم المسلسل الذي تبحث عنه الآن وسأرسل لك الحلقات فوراً."
    )
    await update.message.reply_text(welcome_text)

# البحث وإرسال المسلسل
async def search_series(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip()
    found = False

    for series_name, data in EGYPTIAN_SERIES.items():
        if user_message.lower() in series_name.lower():
            response_text = (
                f"🎬 **المسلسل:** {series_name}\n\n"
                f"📝 **القصة:** {data['story']}\n\n"
                f"👇 **اضغط على الرابط لمشاهدة وتحميل الحلقات:**\n{data['video_id']}"
            )
            await update.message.reply_text(response_text, parse_mode="Markdown")
            found = True
            break
    
    if not found:
        await update.message.reply_text(
            "عذراً، لم أجد هذا المسلسل حالياً. جاري إضافته قريباً! 🍿"
        )

def main():
    # بناء التطبيق وتشغيله
    application = Application.builder().token(TOKEN).build()

    # الأوامر والمستمعين
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_series))

    print("البوت يعمل الآن بنجاح بعد إضافة مسلسل الأسطورة...")
    application.run_polling()

if __name__ == '__main__':
    main()
