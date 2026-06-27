import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"

# قاعدة بيانات المسلسلات من قنوات عامة
MOVIES_DATABASE = {
    "الأسطورة": {
        "aliases": ["الاسطورة", "الأسطوره", "الاسطوره", "اسطورة", "اسطوره"],
        "story": "تدور أحداث المسلسل حول ناصر، شاب خريج كلية الحقوق يسعى للتعيين في النيابة، ولكن بسبب ظروف عائلته وشقيقه رفاعي يتغير مسار حياته تماماً ويدخل في عالم تجارة السلاح والانتقام.",
        
        # 1. 👈 ضع هنا اسم (يوزر) القناة التي تنشر الحلقات (مثال: @ElOstoraChannel)
        "from_chat_id": "@اسم_يوزر_القناة_هنا",  
        
        # 2. 👈 ضع هنا رقم رسالة الحلقة الأولى في القناة (البوت سيكمل باقي الحلقات تلقائياً بالتسلسل!)
        "start_message_id": 154  # استبدل 154 برقم الرسالة الحقيقي للحلقة الأولى
    }
}

# أمر /start بالمقدمة الاحترافية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "مرحبا في بوت مسلسلات وأفلام مصريه 🎬✨\n"
        "الحقوق قصي ⚖️\n\n"
        "اكتب الآن اسم المسلسل أو الفيلم الذي تبحث عنه، وسأعرض لك حلقاته فوراً! 🍿"
    )
    await update.message.reply_text(welcome_text)

# البحث وعرض الأزرار لـ 30 حلقة بشكل ذكي وتلقائي
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
        
        # إنشاء 30 زر تلقائياً (كل سطر 5 أزرار ليناسب شاشة الآيفون تماماً)
        for i in range(1, 31):
            ep_num = str(i)
            callback_data = f"fwd|{actual_name}|{ep_num}"
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
            f"👇 **اختر رقم الحلقة وسيتم توجيه الفيديو لك مباشرة من القناة:**"
        )
        await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text("عذراً، لم يتم العثور على هذا المسلسل حالياً. جاري رفعه وإضافته قريباً! 🔥🍿")

# معالجة الضغط على زر الحلقة وعمل توجيه (Forward) تلقائي ومباشر
async def handle_forward_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data_parts = query.data.split("|")
    if data_parts[0] == "fwd":
        series_name = data_parts[1]
        episode_num = int(data_parts[2]) # تحويل رقم الحلقة لرقم صحيح لعمل الحسبة
        
        if series_name in MOVIES_DATABASE:
            series_data = MOVIES_DATABASE[series_name]
            from_channel = series_data["from_chat_id"]
            
            # حسبة ذكية: نأخذ رقم رسالة البداية ونضيف عليه ترتيب الحلقة المطلوبة
            # حلقة 1 تأخذ الـ start_message_id مباشرة، حلقة 2 تأخذ الرقم التالي، وهكذا
            base_message_id = series_data["start_message_id"]
            target_message_id = base_message_id + (episode_num - 1)
            
            loading_msg = await query.message.reply_text(f"⏳ جاري جلب وتوجيه الحلقة {episode_num} مباشرة...")
            
            try:
                # توجيه الرسالة مباشرة للمستخدم دون روابط
                await context.bot.forward_message(
                    chat_id=query.message.chat_id,
                    from_chat_id=from_channel,
                    message_id=target_message_id
                )
                await loading_msg.delete()
            except Exception as e:
                await loading_msg.edit_text("❌ عذراً، لم أستطع سحب الفيديو. تأكد من يوزر القناة ورقم الرسالة، أو أن القناة عامة.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    application.add_handler(CallbackQueryHandler(handle_forward_choice))

    print("البوت المحدث والذكي يعمل الآن بنجاح على Railway...")
    application.run_polling()

if __name__ == '__main__':
    main()
