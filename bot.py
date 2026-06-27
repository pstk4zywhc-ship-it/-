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

# قاموس ذكي يحتوي على الترجمة، اللفظ بالعربي، ومثال لكل كلمة مع إيموجيات
DICTIONARY_DATA = {
    "hello": {
        "translation": "مرحباً 👋🔥",
        "pronunciation": "هَلُوو 🗣️",
        "example_en": "Hello! How are you today? 🤔",
        "example_ar": "مرحباً! كيف حالك اليوم؟"
    },
    "achieve": {
        "translation": "يحقق / ينجز 🎯💪",
        "pronunciation": "أَشِيفْ 🗣️",
        "example_en": "You can achieve your goals with hard work. 📈",
        "example_ar": "يمكنك تحقيق أهدافك بالعمل الجاد."
    },
    "believe": {
        "translation": "يصدق / يؤمن بـ 🧠✨",
        "pronunciation": "بِيلِيفْ 🗣️",
        "example_en": "Always believe in yourself. 👑",
        "example_ar": "آمن بنفسك دائماً."
    },
    "challenge": {
        "translation": "تحدي ⚔️🔥",
        "pronunciation": "تْشَالِينْجْ 🗣️",
        "example_en": "Learning a new language is a great challenge. 📚",
        "example_ar": "تعلم لغة جديدة هو تحدٍ كبير."
    },
    "improve": {
        "translation": "يحسّن / يطوّر 🚀⚡",
        "pronunciation": "إِمْبْرُوفْ 🗣️",
        "example_en": "Read every day to improve your English. 📖",
        "example_ar": "اقرأ كل يوم لتحسين لغتك الإنجليزية."
    },
    "opportunity": {
        "translation": "فرصة 💎🌟",
        "pronunciation": "أُوبُرْتْيُونِيتِي 🗣️",
        "example_en": "Don't miss this opportunity. 🛑",
        "example_ar": "لا تضيع هذه الفرصة."
    },
    "success": {
        "translation": "نجاح 🏆👑",
        "pronunciation": "سَكْسِيسْ 🗣️",
        "example_en": "Confidence is the key to success. 🔑",
        "example_ar": "الثقة هي مفتاح النجاح."
    },
    "focus": {
        "translation": "يركز 👁️🔍",
        "pronunciation": "فُوكَسْ 🗣️",
        "example_en": "You need to focus on your study. 📝",
        "example_ar": "تحتاج إلى التركيز على دراستك."
    },
    "same": {
        "translation": "نفس الشيء / مِثْل 🔀👥",
        "pronunciation": "سِيوْم 🗣️",
        "example_en": "We have the same opinion. 🤝",
        "example_ar": "لدينا نفس الرأي."
    }
}

# أمر /start بترحيب احترافي باسمك
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🇺🇸 ⚔️ **مرحباً بك في بوت الترجمة والتعليم الاحترافي** 🇬🇧\n"
        "👑 **بإشراف المطور: قصي** 👑\n\n"
        "🤖 **ماذا يمكنني أن أفعل؟**\n"
        "1️⃣ **المعلم الذكي:** أرسل لي أي كلمة إنجليزية (مثل: *same* أو *Success*) وسأعطيك معناها ونطقها فوراً!\n"
        "2️⃣ **القسم التعليمي:** اضغط على الأزرار بالأسفل لاستكشاف الدروس السريعة 👇"
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 أهم الكلمات الشائعة", callback_data="edu_words"),
         InlineKeyboardButton("🗣️ محادثات يومية", callback_data="edu_conv")],
        [InlineKeyboardButton("📐 قواعد أساسية سريعة", callback_data="edu_grammar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# معالجة الكلمات وعرض النطق والمثال بالأسلوب الجديد
async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip().lower()
    
    if user_text in DICTIONARY_DATA:
        word_info = DICTIONARY_DATA[user_text]
        
        # الترتيب المباشر الذي طلبته مع الإيموجيات
        response = (
            f"🇺🇸 **الكلمة:** `{user_text.upper()}`\n\n"
            f"🎈 **معناها:** {word_info['translation']}\n"
            f"📢 **وتلفظ:** {word_info['pronunciation']}\n\n"
            f"📌 **مثال توضيحي (Example):**\n"
            f"• `{word_info['example_en']}`\n"
            f"• _ترجمة المثال:_ {word_info['example_ar']}"
        )
    else:
        # النصيحة تظهر هنا بالأسفل فقط تحت التنبيه في حال عدم وجود الكلمة
        response = (
            f"❌ **عذراً، هذه الكلمة غير مضافة في القاموس حالياً!**\n\n"
            f"💡 *نصيحة المطور قصي:* جرب كتابة كلمات إنجليزية مضافة مثل: **same** أو **success** أو **improve** لتشاهد نظام النطق الاحترافي الحين! ✨"
        )
    
    await update.message.reply_text(response, parse_mode="Markdown")

# معالجة الضغط على أزرار التعليم
async def handle_edu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "edu_words":
        words_text = (
            "🎯 **أهم الكلمات المتاحة (اكتبها للبوت لترى النطق والمعنى والمثال!):**\n\n"
            "• **same** ➡️ نفس الشيء\n"
            "• **Success** ➡️ نجاح\n"
            "• **Improve** ➡️ يحسّن\n"
            "• **Focus** ➡️ يركز\n"
            "• **Achieve** ➡️ يحقق\n"
            "• **Believe** ➡️ يصدق"
        )
        await query.message.reply_text(words_text, parse_mode="Markdown")
        
    elif action == "edu_conv":
        conv_text = (
            "🗣️ **محادثات يومية هامة:**\n\n"
            "🤝 **للترحيب والتعارف:**\n"
            "• Nice to meet you ➡️ فرصة سعيدة.\n"
            "• Where are you from? ➡️ من أين أنت؟\n\n"
            "☕ **في الكافيه أو المطعم:**\n"
            "• Can I have the menu, please? ➡️ هل يمكنني الحصول على القائمة؟"
        )
        await query.message.reply_text(conv_text, parse_mode="Markdown")
        
    elif action == "edu_grammar":
        grammar_text = (
            "📐 **قاعدة ذهبية سريعة (الزمن المضارع البسيط):**\n\n"
            "• مع الضمائر *(I, They, We, You)* ➡️ نضع الفعل كما هو.\n"
            "  *مثال:* I play football.\n\n"
            "• مع الضمائر *(He, She, It)* ➡️ نضيف **S** للفعل.\n"
            "  *مثال:* He plays football."
        )
        await query.message.reply_text(grammar_text, parse_mode="Markdown")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_translation))
    application.add_handler(CallbackQueryHandler(handle_edu_buttons))

    print("بوت المعلم الذكي المحدث يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
