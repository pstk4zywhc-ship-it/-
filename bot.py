import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# تفعيل نظام تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"

# قاعدة بيانات المسلسلات والأفلام بالأزرار والحلقات
# تنبيه: استبدل الروابط الافتراضية (مثل https://t.me/...) بروابط الحلقات الحقيقية من قناتك لكي تفتح مع الناس
MOVIES_DATABASE = {
    "الأسطورة": {
        "aliases": ["الاسطورة", "الأسطوره", "الاسطوره", "اسطورة", "اسطوره"],
        "story": "تدور أحداث المسلسل حول ناصر، شاب خريج كلية الحقوق يسعى للتعيين في النيابة، ولكن بسبب ظروف شقيقه رفاعي يتغير مسار حياته تماماً ويدخل في عالم تجارة السلاح والانتقام.",
        "episodes": {
            "الحلقة 1": "https://t.me/c/123456789/1",  # ضع رابط الحلقة 1 الحقيقي هنا
            "الحلقة 2": "https://t.me/c/123456789/2",  # ضع رابط الحلقة 2 الحقيقي هنا
            "الحلقة 3": "https://t.me/c/123456789/3",  # ضع رابط الحلقة 3 الحقيقي هنا
            "الحلقة 4": "https://t.me/c/123456789/4",  # ضع رابط الحلقة 4 الحقيقي هنا
            "الحلقة 5": "https://t.me/c/123456789/5",  # ضع رابط الحلقة 5 الحقيقي هنا
        }
    },
    "جعفر العمدة": {
        "aliases": ["جعفر", "العمدة", "العامده", "جعفر العمده"],
        "story": "تدور الأحداث في إطار اجتماعي شعبي حول جعفر العمدة الذي يعيش في حي السيدة زينب ويمتلك شركات للمقاولات ويبحث عن ابنه المفقود منذ 19 عاماً.",
        "episodes": {
            "الحلقة 1": "https://t.me/c/123456789/6",
            "الحلقة 2": "https://t.me/c/123456789/7",
            "الحلقة 3": "https://t.me/c/123456789/8",
        }
    }
}

# أمر /start بالمقدمة الاحترافية لقصي
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "مرحبا في بوت مسلسلات وأفلام مصريه 🎬✨\n"
        "الحقوق قصي ⚖️\n\n"
        "اكتب الآن اسم المسلسل أو الفيلم الذي تبحث عنه، وسأعرض لك حلقاته فوراً! 🍿"
    )
    await update.message.reply_text(welcome_text)

# البحث وعرض الحلقات على شكل أزرار
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip().lower()
    found_series = None
    actual_name = ""

    for item_name, data in MOVIES_DATABASE.items():
        if user_message in item_name.lower() or any(alias in user_message for alias in data["aliases"]):
            found_series = data
            actual_name = item_name
            break
    
    if found_series:
        # إنشاء الأزرار التفاعلية للحلقات
        keyboard = []
        # ترتيب الأزرار لكي تظهر بشكل منظم (كل زرين بجانب بعضهما)
        row = []
        for ep_name in found_series["episodes"].keys():
            # نرسل اسم المسلسل واسم الحلقة داخل الـ callback_data ليعرف البوت ماذا اختار المستخدم
            callback_data = f"ep|{actual_name}|{ep_name}"
            row.append(InlineKeyboardButton(ep_name, callback_data=callback_data))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
            
        reply_markup = InlineKeyboardMarkup(keyboard)

        response_text = (
            f"🎬 **المسلسل:** {actual_name}\n\n"
            f"📝 **القصة:** {found_series['story']}\n\n"
            f"👇 **اختر الحلقة التي تريد مشاهدتها من الأزرار بالأسفل:**"
        )
        await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "عذراً، لم يتم العثور على هذا المسلسل حالياً. جاري رفعه وإضافته قريباً! 🔥🍿"
        )

# معالجة الضغط على أزرار الحلقات
async def handle_episode_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer() # تنبيه التليجرام أن الضغطة تمت
    
    data_parts = query.data.split("|")
    if data_parts[0] == "ep":
        series_name = data_parts[1]
        episode_name = data_parts[2]
        
        # جلب رابط الحلقة من قاعدة البيانات
        if series_name in MOVIES_DATABASE and episode_name in MOVIES_DATABASE[series_name]["episodes"]:
            ep_link = MOVIES_DATABASE[series_name]["episodes"][episode_name]
            
            reply_text = (
                f"🍿 **مسلسل:** {series_name}\n"
                f"📌 **{episode_name} جاهزة الآن للمشاهدة!**\n\n"
                f"🔗 [اضغط هنا لمشاهدة الحلقة مباشرة]({ep_link})\n\n"
                "🛡️ _الحقوق محفوظة لـ قصي_"
            )
            await query.message.reply_text(reply_text, parse_mode="Markdown", disable_web_page_preview=False)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    # مستمع خاص بالضغط على الأزرار
    application.add_handler(CallbackQueryHandler(handle_episode_choice))

    print("البوت الاحترافي المطور بالأزرار لـ (قصي) يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
