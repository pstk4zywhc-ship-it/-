import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# مكتبة الترجمة الذكية للجمل والكلمات (تأكد من إضافتها لملف requirements.txt)
from deep_translator import GoogleTranslator

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"

# قاعدة بيانات مخصصة للكلمات الشائعة في وضع المعلم الذكي لتعطي نطقاً تقريبياً
SMART_DICTIONARY = {
    "hello": {"pron": "هَلُوو 🗣️", "ex_en": "Hello! How are you today? 🤔", "ex_ar": "مرحباً! كيف حالك اليوم؟"},
    "same": {"pron": "سِيوْم 🗣️", "ex_en": "We have the same opinion. 🤝", "ex_ar": "لدينا نفس الرأي."},
    "opinion": {"pron": "أُوبِينْيُوْن 🗣️", "ex_en": "In my opinion, you are right. 👍", "ex_ar": "في رأيي، أنت على حق."},
    "success": {"pron": "سَكْسِيسْ 🗣️", "ex_en": "Confidence is the key to success. 🔑", "ex_ar": "الثقة هي مفتاح النجاح."},
    "improve": {"pron": "إِمْبْرُوفْ 🗣️", "ex_en": "Practice every day to improve. 📖", "ex_ar": "تدرب كل يوم لتحسين مستواك."},
    "the": {"pron": "ذَا 🗣️", "ex_en": "The book is on the table. 📘", "ex_ar": "الكتاب على الطاولة."},
    "potato": {"pron": "بُوتِيتُو 🗣️", "ex_en": "I love eating fried potatoes! 🍟", "ex_ar": "أنا أحب أكل البطاطا المقلية!"}
}

# إعداد زر القائمة الأزرق التلقائي (Menu)
async def post_init(application: Application) -> None:
    commands = [BotCommand("start", "🔄 فتح الواجهة الرئيسية والاختيارات")]
    await application.bot.set_my_commands(commands)

# أمر /start يرسل النص والأزرار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['mode'] = 'smart_teacher'
    
    welcome_text = (
        "✨ **مرحباً بك في بوت الترجمة الاحترافي الخارق** ✨\n"
        "👑 **بإشراف المطور قصي** 👑\n\n"
        "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي (نطق + أمثلة)_\n\n"
        "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
    )
    
    keyboard = [
        [InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar")],
        [InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en")],
        [InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# معالجة الضغط على أزرار الخيارات وتغيير وضع البوت
async def handle_mode_switch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "mode_en_to_ar":
        context.user_data['mode'] = 'en_to_ar'
        await query.message.reply_text("🔄 **تم تفعيل الوضع:** [ إنجليزي ⬅️ عربي 🇵🇸 ]\n📥 أرسل لي أي كلمة أو جملة بالإنجليزية وسأترجمها فوراً!")
    
    elif query.data == "mode_ar_to_en":
        context.user_data['mode'] = 'ar_to_en'
        await query.message.reply_text("🔄 **تم تفعيل الوضع:** [ عربي 🇵🇸 ⬅️ إنجليزي ]\n📥 أرسل لي أي كلمة أو جملة بالعربية وسأترجمها فوراً!")
        
    elif query.data == "mode_smart":
        context.user_data['mode'] = 'smart_teacher'
        await query.message.reply_text("🧠 **تم تفعيل الوضع:** [ المعلم الذكي ]\n📥 أرسل الكلمة الإنجليزية لترى النطق بالعربي والأمثلة الكاملة!")

# معالجة الرسائل وترجمتها ديناميكياً (كلمات وجمل)
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip()
    current_mode = context.user_data.get('mode', 'smart_teacher')
    
    # رسالة انتظار خفيفة للمستخدم
    waiting_msg = await update.message.reply_text("⏳ جاري الترجمة الاحترافية...")
    
    try:
        # 1️⃣ خيار: إنجليزي إلى عربي (يدعم جمل وكلمات)
        if current_mode == 'en_to_ar':
            translated = GoogleTranslator(source='en', target='ar').translate(user_text)
            res = f"🇺🇸 **النص الأصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة المباشرة:**\n*{translated}*"
            await waiting_msg.edit_text(res, parse_mode="Markdown")

        # 2️⃣ خيار: عربي إلى إنجليزي (يدعم جمل وكلمات)
        elif current_mode == 'ar_to_en':
            translated = GoogleTranslator(source='ar', target='en').translate(user_text)
            res = f"🇵🇸 **النص الأصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة المباشرة:**\n*{translated}*"
            await waiting_msg.edit_text(res, parse_mode="Markdown")

        # 3️⃣ خيار: المعلم الذكي (للكلمات والجمل)
        elif current_mode == 'smart_teacher':
            # إذا كان النص عبارة عن كلمة واحدة بدون مسافات
            if " " not in user_text:
                word_clean = user_text.lower()
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                
                # التحقق إذا كانت الكلمة في القاموس الثابت لأخذ النطق والأمثلة المخصصة
                if word_clean in SMART_DICTIONARY:
                    info = SMART_DICTIONARY[word_clean]
                    pron = info['pron']
                    ex_en = info['ex_en']
                    ex_ar = info['ex_ar']
                else:
                    pron = "متاح عبر الاستماع الصوتي 🗣️"
                    ex_en = f"I am learning the word '{user_text}'."
                    ex_ar = f"أنا أتعلم كلمة '{user_text}'."
                
                response = (
                    f"🇺🇸 **الكلمة:** `{user_text.upper()}`\n\n"
                    f"🎈 **معناها:** {translated}\n"
                    f"📢 **وتلفظ تقريباً:** {pron}\n\n"
                    f"📌 **مثال توضيحي (Example):**\n"
                    f"• `{ex_en}`\n"
                    f"• _ترجمة المثال:_ {ex_ar}\n\n"
                    f"--- \n"
                    f"💡 _نصيحة المطور قصي:_ استمر في إرسال الكلمات لتقوية لغتك! ✨"
                )
            else:
                # إذا كانت جملة كاملة في وضع المعلم الذكي
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                response = (
                    f"📝 **تحليل الجملة الذكي:**\n\n"
                    f"🇺🇸 **الجملة الأصلية:** `{user_text}`\n"
                    f"🇵🇸 **ترجمتها الكاملة:** *{translated}*\n\n"
                    f"💡 _نصيحة المطور قصي:_ حاول تفكيك الجملة لحفظ الكلمات الفردية! 🚀"
                )
            await waiting_msg.edit_text(response, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"Error during translation: {e}")
        await waiting_msg.edit_text("❌ عذراً، حدث خطأ أثناء الاتصال بمحرك الترجمة. حاول مجدداً بعد ثوانٍ!")

def main():
    application = Application.builder().token(TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_mode_switch))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("بوت قصي للترجمة الفورية للجمل والكلمات يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
