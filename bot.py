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

# قاعدة بيانات المسلسلات
# تذكر: يجب ملء أكواد الفيديوهات (File ID) الحقيقية لكل حلقة لكي يرسلها البوت مباشرة
MOVIES_DATABASE = {
    "الأسطورة": {
        "aliases": ["الاسطورة", "الأسطوره", "الاسطوره", "اسطورة", "اسطوره"],
        "story": "تدور أحداث المسلسل حول ناصر، شاب خريج كلية الحقوق يسعى للتعيين في النيابة، ولكن بسبب ظروف شقيقه رفاعي يتغير مسار حياته تماماً ويدخل في عالم تجارة السلاح والانتقام.",
        "episodes": {
            # ضع هنا الـ File ID الخاص بكل حلقة بدلاً من الأكواد التجريبية بالأسفل:
            "1": "AgACAgQAAx0C...", 
            "2": "AgACAgQAAx0C...",
            "3": "AgACAgQAAx0C...",
            # يمكنك إكمال بقية الحلقات حتى 30 بنفس الطريقة هنا...
        }
    },
    "جعفر العمدة": {
        "aliases": ["جعفر", "العمدة", "العامده", "جعفر العمده"],
        "story": "تدور الأحداث في إطار اجتماعي شعبية حول جعفر العمدة الذي يعيش في حي السيدة زينب ويبحث عن ابنه المفقود منذ سنوات.",
        "episodes": {
            "1": "AgACAgQAAx0C...",
            "2": "AgACAgQAAx0C...",
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

# البحث وعرض الأزرار لـ 30 حلقة بشكل تلقائي ومنظم
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
        keyboard = []
        row = []
        
        # إنشاء 30 زر تلقائياً وبشكل منظم جداً (كل سطر يحتوي على 5 أزرار لتناسب شاشة الآيفون)
        for i in range(1, 31):
            ep_num = str(i)
            callback_data = f"ep|{actual_name}|{ep_num}"
            row.append(InlineKeyboardButton(f"حلقة {ep_num}", callback_data=callback_data))
            
            if len(row) == 5:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
            
        reply_markup = InlineKeyboardMarkup(keyboard)

        response_text = (
            f"🎬 **المسلسل:** {actual_name}\n\n"
            f"📝 **القصة:** {found_series['story']}\n\n"
            f"👇 **اختر رقم الحلقة التي تريد مشاهدتها وسيتم إرسال الفيديو لك مباشرة هنا:**"
        )
        await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "عذراً، لم يتم العثور على هذا المسلسل حالياً. جاري رفعه وإضافته قريباً! 🔥🍿"
        )

# معالجة الضغط على زر الحلقة وإرسال الفيديو مباشرة
async def handle_episode_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data_parts = query.data.split("|")
    if data_parts[0] == "ep":
        series_name = data_parts[1]
        episode_num = data_parts[2]
        
        if series_name in MOVIES_DATABASE and episode_num in MOVIES_DATABASE[series_name]["episodes"]:
            video_file_id = MOVIES_DATABASE[series_name]["episodes"][episode_num]
            
            # إرسال رسالة انتظار سريعة للمستخدم
            loading_msg = await query.message.reply_text(f"⏳ جاري تحميل وإرسال الحلقة {episode_num} مباشرة، يرجى الانتظار ثواني...")
            
            try:
                # إرسال الفيديو مباشرة باستخدام الـ File ID
                await query.message.reply_video(
                    video=video_file_id,
                    caption=f"🍿 مسلسل: {series_name} - الحلقة {episode_num}\n\n🛡️ _الحقوق محفوظة لـ قصي_"
                )
                # حذف رسالة الانتظار بعد إرسال الفيديو بنجاح
                await loading_msg.delete()
            except Exception as e:
                # إذا كان الكود تجريبياً أو غير صحيح، سيظهر تنبيه
                await loading_msg.edit_text("❌ عذراً، لم يتم العثور على ملف الفيديو الحقيقي لهذه الحلقة في الخادم حالياً.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    application.add_handler(CallbackQueryHandler(handle_episode_choice))

    print("البوت الاحترافي الشامل (30 حلقة فيديو مباشر) لـ (قصي) يعمل...")
    application.run_polling()

if __name__ == '__main__':
    main()
