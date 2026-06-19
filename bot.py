import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"

# قاعدة بيانات المسلسلات والأفلام الاحترافية
# ملاحظة: استبدل الروابط الافتراضية بروابط قنواتك الحقيقية لكي تفتح مع المشتركين بدون مشاكل
MOVIES_DATABASE = {
    "الأسطورة": {
        "aliases": ["الاسطورة", "الأسطوره", "الاسطوره", "اسطورة", "اسطوره"],
        "story": "تدور أحداث المسلسل حول ناصر، شاب خريج كلية الحقوق يسعى للتعيين في النيابة، ولكن بسبب ظروف عائلته وشقيقه رفاعي يتغير مسار حياته تماماً ويدخل في عالم تجارة السلاح والانتقام.",
        "link": "https://t.me/c/123456789/4"  # ضع هنا رابط قناتك الحقيقي لمسلسل الأسطورة
    },
    "جعفر العمدة": {
        "aliases": ["جعفر", "العمدة", "العامده", "جعفر العمده"],
        "story": "تدور الأحداث في إطار اجتماعي شعبي حول جعفر العمدة الذي يعيش في حي السيدة زينب ويمتلك شركات للمقاولات ويبحث عن ابنه المفقود منذ 19 عاماً.",
        "link": "https://t.me/c/123456789/1"   # ضع هنا رابط قناتك الحقيقي لجعفر العمدة
    },
    "الاختيار": {
        "aliases": ["اختيار", "الاختيار 1", "الاختيار 2"],
        "story": "يتناول العمل بطولات رجال القوات المسلحة والشرطة المصرية والتضحيات الكبيرة التي يقدمونها لحماية الوطن.",
        "link": "https://t.me/c/123456789/2"
    },
    "الكبير أوي": {
        "aliases": ["الكبير", "جوني", "حزلقوم", "المزاريطة"],
        "story": "مغامرات كوميدية في قرية المزاريطة بين الكبير وجوني وحزلقوم ومواقفهم الطريفة مع أهل القرية.",
        "link": "https://t.me/c/123456789/3"
    }
}

# أمر /start بالمقدمة الجديدة الاحترافية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "مرحبا في بوت مسلسلات وأفلام مصريه 🎬✨\n"
        "الحقوق قصي ⚖️\n\n"
        "اكتب الآن اسم المسلسل أو الفيلم الذي تبحث عنه، وسأرسل لك الحلقات فوراً! 🍿"
    )
    await update.message.reply_text(welcome_text)

# البحث الذكي عن المسلسلات
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip().lower()
    found = False

    for item_name, data in MOVIES_DATABASE.items():
        # التحقق إذا كان النص المكتوب يطابق الاسم الأساسي أو أي من الأسماء البديلة (Aliases)
        if user_message in item_name.lower() or any(alias in user_message for alias in data["aliases"]):
            response_text = (
                f"🎬 **المسلسل:** {item_name}\n\n"
                f"📝 **القصة:** {data['story']}\n\n"
                f"👇 **اضغط على الرابط لمشاهدة وتحميل الحلقات:**\n{data['link']}\n\n"
                "🛡️ _الحقوق محفوظة لـ قصي_"
            )
            await update.message.reply_text(response_text, parse_mode="Markdown")
            found = True
            break
    
    if not found:
        await update.message.reply_text(
            "عذراً،
