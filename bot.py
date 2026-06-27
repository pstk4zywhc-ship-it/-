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

# قاموس ذكي يحتوي على الترجمة، اللفظ بالعربي، ومثال لكل كلمة
DICTIONARY_DATA = {
    "hello": {
        "translation": "مرحباً",
        "pronunciation": "هَلُوو",
        "example_en": "Hello! How are you today?",
        "example_ar": "مرحباً! كيف حالك اليوم؟"
    },
    "achieve": {
        "translation": "يحقق / ينجز",
        "pronunciation": "أَشِيفْ",
        "example_en": "You can achieve your goals with hard work.",
        "example_ar": "يمكنك تحقيق أهدافك بالعمل الجاد."
    },
    "believe": {
        "translation": "يصدق / يؤمن بـ",
        "pronunciation": "بِيلِيفْ",
        "example_en": "Always believe in yourself.",
        "example_ar": "آمن بنفسك دائماً."
    },
    "challenge": {
        "translation": "تحدي",
        "pronunciation": "تْشَالِينْجْ",
        "example_en": "Learning a new language is a great challenge.",
        "example_ar": "تعلم لغة جديدة هو تحدٍ كبير."
    },
    "improve": {
        "translation": "يحسّن / يطوّر",
        "pronunciation": "إِمْبْرُوفْ",
        "example_en": "Read every day to improve your English.",
        "example_ar": "اقرأ كل يوم لتحسين لغتك الإنجليزية."
    },
    "opportunity": {
        "translation": "فرصة",
        "pronunciation": "أُوبُرْتْيُونِيتِي",
        "example_en": "Don't miss this opportunity.",
        "example_ar": "لا تضيع هذه الفرصة."
    },
    "success": {
        "translation": "نجاح",
        "pronunciation": "سَكْسِيسْ",
        "example_en": "Confidence is the key to success.",
        "example_ar": "الثقة هي مفتاح النجاح."
    },
    "focus": {
        "translation": "يركز",
        "pronunciation": "فُوكَسْ",
        "example_en": "You need to focus on your study.",
        "example_ar": "تحتاج إلى التركيز على دراستك."
    },
    "experience": {
        "translation": "خبرة / تجربة",
        "pronunciation": "إِكْسْبِيرِيَنْسْ",
        "example_en": "He has five years of experience in programming.",
        "example_ar": "لديه خمس سنوات من الخبرة في البرمجة."
    },
    "decision": {
        "translation": "قرار",
        "pronunciation": "دِيسِيجَنْ",
        "example_en": "It was a very difficult decision.",
        "example_ar": "لقد كان قراراً صعباً للغاية."
    },
    "confidence": {
        "translation": "ثقة",
        "pronunciation": "كُونْفِيدَنْسْ",
        "example_en": "She speaks English with confidence.",
        "example_ar": "هي تتحدث الإنجليزية بثقة."
    },
    "thanks": {
        "translation": "شكراً",
        "pronunciation": "ثَانْكْسْ",
        "example_en": "Thanks for your help.",
        "example_ar": "شكراً على مساعدتك."
    },
    "please": {
        "translation": "من فضلك",
        "pronunciation": "بْلِيزْ",
        "example_en": "Open the door, please.",
        "example_ar": "افتح الباب، من فضلك."
    }
}

# أمر /start بترحيب احترافي باسمك
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🇺🇸 ⚔️ **مرحباً بك في بوت الترجمة والتعليم الاحترافي** 🇬🇧\n"
        "👑 **بإشراف المطور: قصي** 👑\n\n"
        "🤖 **ماذا يمكنني أن أفعل؟**\n"
        "1️⃣ **المعلم الذكي:** أرسل لي أي كلمة إنجليزية (مثل: *Success* أو *Improve*) وسأعطيك ترجمتها، طريقة نطقها بالعربي، ومثالاً عليها!\n"
        "2️⃣ **القسم التعليمي:** اضغط على الأزرار بالأسفل لاستكشاف الدروس السريعة 👇"
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 أهم الكلمات الشائعة", callback_data="edu_words"),
         InlineKeyboardButton("🗣️ محادثات يومية", callback_data="edu_conv")],
        [InlineKeyboardButton("📐 قواعد أساسية سريعة", callback_data="edu_grammar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# معالجة الكلمات وعرض النطق والمثال تلقائياً
async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip().lower()
    
    # التحقق من وجود الكلمة في القاموس الذكي
    if user_text in DICTIONARY_DATA:
        word_info = DICTIONARY_DATA[user_text]
        
        response = (
            f"🇺🇸 **الكلمة:** `{user_text.capitalize()}`\n"
            f"✨ **الترجمة:** {word_info['translation']}\n"
            f"🗣️ **طريقة اللفظ بالعربي:** [ *{word_info['pronunciation']}* ]\n\n"
            f"📝 **مثال عليها (Example):**\n"
            f"• `{word_info['example_en']}`\n"
            f"• _ترجمة المثال:_ {word_info['example_ar']}"
        )
    else:
        # إذا كانت كلمة عربية أو كلمة غير مضافة بعد
        response = (
            f"🔄 **جاري استقبال الكلمة:**\n\n"
            f"📥 كتبت: *\"{user_text}\"*\n\n"
            f"💡 _نصيحة:_ جرب كتابة كلمات إنجليزية مثل: **success** أو **improve** أو **focus** لتشاهد نظام النطق الأمثلة الاحترافي!"
        )
    
    await update.message.reply_text(response, parse_mode="Markdown")

# معالجة الضغط على أزرار التعليم
async def handle_edu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "edu_words":
        words_text = (
            "🎯 **أهم الكلمات الشائعة (اكتب أي كلمة منها للبوت ليرسل لك نطقها ومثالاً عليها!):**\n\n"
            "• **Achieve** ➡️ يحقق\n"
            "• **Believe** ➡️ يصدق / يؤمن\n"
            "• **Challenge** ➡️ تحدي\n"
            "• **Improve** ➡️ يحسّن\n"
            "• **Opportunity** ➡️ فرصة\n"
            "• **Success** ➡️ نجاح\n"
            "• **Focus** ➡️ يركز"
        )
        await query.message.reply_text(words_text, parse_mode="Markdown")
        
    elif action == "edu_conv":
        conv_text = (
            "🗣️ **محادثات يومية هامة:**\n\n"
            "🤝 **للترحيب والتعارف:**\n"
            "• Nice to meet you ➡️ فرصة سعيدة.\n"
            "• Where are you from? ➡️ من أين أنت؟\n\n"
            "☕ **في الكافيه أو المطعم:**\n"
            "• Can I have the menu, please? ➡️ هل يمكنني الحصول على القائمة؟\n"
            "• Keep the change ➡️ احتفظ بالباقي."
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

    print("بوت المعلم الذكي لـ (قصي) يعمل الآن بنجاح...")
    application.run_polling()

if __name__ == '__main__':
    main()
