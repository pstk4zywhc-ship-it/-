import os
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"

# رابط صورة ترحيبية احترافية للتعليم والترجمة
WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=800"

# قاعدة البيانات الشاملة للمعلم الذكي والترجمة السريعة
DICTIONARY_DATA = {
    "hello": {"tr_ar": "مرحباً 👋", "tr_en": "hello", "pron": "هَلُوو 🗣️", "ex_en": "Hello! How are you today? 🤔", "ex_ar": "مرحباً! كيف حالك اليوم؟"},
    "same": {"tr_ar": "نفس الشيء / مِثْل 🔀", "tr_en": "same", "pron": "سِيوْم 🗣️", "ex_en": "We have the same opinion. 🤝", "ex_ar": "لدينا نفس الرأي."},
    "opinion": {"tr_ar": "رأي / وجهة نظر 💭", "tr_en": "opinion", "pron": "أُوبِينْيُوْن 🗣️", "ex_en": "In my opinion, you are right. 👍", "ex_ar": "في رأيي، أنت على حق."},
    "success": {"tr_ar": "نجاح 🏆", "tr_en": "success", "pron": "سَكْسِيسْ 🗣️", "ex_en": "Confidence is the key to success. 🔑", "ex_ar": "الثقة هي مفتاح النجاح."},
    "improve": {"tr_ar": "يحسّن / يطوّر 🚀", "tr_en": "improve", "pron": "إِمْبْرُوفْ 🗣️", "ex_en": "Practice every day to improve. 📖", "ex_ar": "تدرب كل يوم لتحسين مستواك."},
    "the": {"tr_ar": "الـ (أداة التعريف) 🌐", "tr_en": "the", "pron": "ذَا 🗣️", "ex_en": "The book is on the table. 📘", "ex_ar": "الكتاب على الطاولة."},
    "potato": {"tr_ar": "بطاطا 🥔", "tr_en": "potato", "pron": "بُوتِيتُو 🗣️", "ex_en": "I love eating fried potatoes! 🍟", "ex_ar": "أنا أحب أكل البطاطا المقلية!"}
}

# قاموس سريع للتحويل العكسي (من عربي إلى إنجليزي)
ARABIC_TO_ENGLISH = {
    "مرحبا": "Hello / Welcome 👋",
    "نفس الشيء": "Same 🔀",
    "راي": "Opinion 💭",
    "رأيي": "In my opinion 💭",
    "نجاح": "Success 🏆",
    "تطوير": "Improvement / Development 🚀",
    "بطاطا": "Potato 🥔"
}

# دالة ذكية لتوليد نطق وترجمة تقريبية لأي كلمة خارج القاموس
def automatic_translator(word):
    pron = word
    pron = re.sub(r'tion', 'شَنْ', pron)
    pron = re.sub(r'ee|ea', 'ِ يـ', pron)
    pron = re.sub(r'oo', 'ُ و', pron)
    pron = re.sub(r'sh', 'شْ', pron)
    pron = re.sub(r'ch', 'تْشْ', pron)
    pron = re.sub(r'th', 'ذْ', pron)
    return {
        "tr_ar": "كلمة جديدة (ترجمة تلقائية) 📚",
        "pron": f"{pron.upper()} 🗣️",
        "ex_en": f"Let's learn the word '{word}'! ⭐",
        "ex_ar": f"فلنتعلم كلمة '{word}'!"
    }

# إعداد زر القائمة الأزرق التلقائي (Menu)
async def post_init(application: Application) -> None:
    commands = [BotCommand("start", "🔄 فتح الواجهة الرئيسية والاختيارات")]
    await application.bot.set_my_commands(commands)

# أمر /start مع الصورة والواجهة الاحترافية بعلم فلسطين 🇵🇸
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['mode'] = 'smart_teacher'
    
    welcome_text = (
        "🇺🇸 **WELCOME TO THE PROFESSIONAL TRANSLATOR BOT** 🇬🇧\n"
        "✨ **مرحباً بك في بوت الترجمة الاحترافي الخارق** ✨\n"
        "👑 **By Developer: Qusai | بإشراف المطور قصي** 👑\n\n"
        "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي (نطق + أمثلة)_\n\n"
        "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
    )
    
    # تم وضع علم فلسطين 🇵🇸 في الأزرار هنا
    keyboard = [
        [InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar")],
        [InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en")],
        [InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=WELCOME_IMAGE_URL,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# معالجة الضغط على أزرار الخيارات وتغيير وضع البوت
async def handle_mode_switch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "mode_en_to_ar":
        context.user_data['mode'] = 'en_to_ar'
        await query.message.reply_text("🔄 **تم تفعيل الوضع:** [ إنجليزي ⬅️ عربي 🇵🇸 ]\n📥 أرسل لي أي كلمة بالإنجليزية وسأعطيك معناها المباشر فوراً!")
    
    elif query.data == "mode_ar_to_en":
        context.user_data['mode'] = 'ar_to_en'
        await query.message.reply_text("🔄 **تم تفعيل الوضع:** [ عربي 🇵🇸 ⬅️ إنجليزي ]\n📥 أرسل لي أي كلمة بالعربية وسأعطيك ترجمتها بالإنجليزية فوراً!")
        
    elif query.data == "mode_smart":
        context.user_data['mode'] = 'smart_teacher'
        await query.message.reply_text("🧠 **تم تفعيل الوضع:** [ المعلم الذكي ]\n📥 أرسل الكلمة الإنجليزية لترى النطق بالعربي والأمثلة الكاملة!")

# معالجة الرسائل بناءً على الخيار المختار
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip().lower()
    current_mode = context.user_data.get('mode', 'smart_teacher')
    
    # 1️⃣ خيار: إنجليزي إلى عربي مباشر
    if current_mode == 'en_to_ar':
        if user_text in DICTIONARY_DATA:
            res = f"🇺🇸 `{user_text.upper()}` ➡️ 🇵🇸 *معناها:* {DICTIONARY_DATA[user_text]['tr_ar']}"
        else:
            res = f"🎯 *ترجمة تقريبية للكلمة:* {user_text} ➡️ تعني كلمة إنجليزية جديدة."
        await update.message.reply_text(res, parse_mode="Markdown")

    # 2️⃣ خيار: عربي إلى إنجليزي مباشر
    elif current_mode == 'ar_to_en':
        clean_text = user_text.replace("أ", "ا").replace("إ", "ا")
        if clean_text in ARABIC_TO_ENGLISH:
            res = f"🇵🇸 *{update.message.text}* ➡️ 🇺🇸 ` {ARABIC_TO_ENGLISH[clean_text]} `"
        else:
            res = f"✨ لم أجد الكلمة بدقة، تأكد من كتابتها بشكل صحيح (مثال: بطاطا، مرحبا، نجاح)."
        await update.message.reply_text(res, parse_mode="Markdown")

    # 3️⃣ خيار: المعلم الذكي
    elif current_mode == 'smart_teacher':
        if user_text in DICTIONARY_DATA:
            word_info = DICTIONARY_DATA[user_text]
        else:
            word_info = automatic_translator(user_text)
            
        response = (
            f"🇺🇸 **الكلمة:** `{user_text.upper()}`\n\n"
            f"🎈 **معناها:** {word_info['tr_ar']}\n"
            f"📢 **وتلفظ:** {word_info['pron']}\n\n"
            f"📌 **مثال توضيحي (Example):**\n"
            f"• `{word_info['ex_en']}`\n"
            f"• _ترجمة المثال:_ {word_info['ex_ar']}\n\n"
            f"--- \n"
            f"💡 _نصيحة المطور قصي:_ استمر في إرسال الكلمات لتقوية لغتك! ✨"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

def main():
    application = Application.builder().token(TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_mode_switch))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("البوت الخارق بعلم فلسطين يعمل الآن بنجاح لقصي...")
    application.run_polling()

if __name__ == '__main__':
    main()
