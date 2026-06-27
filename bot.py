import os
import logging
import telebot
from telebot import types
from deep_translator import GoogleTranslator

# تفعيل تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"
bot = telebot.TeleBot(TOKEN)

# تخزين وضع المستخدم (الافتراضي: المعلم الذكي)
user_modes = {}

# قاعدة بيانات الكلمات الشائعة للمعلم الذكي
SMART_DICTIONARY = {
    "hello": {"pron": "هَلُوو 🗣️", "ex_en": "Hello! How are you today? 🤔", "ex_ar": "مرحباً! كيف حالك اليوم؟"},
    "same": {"pron": "سِيوْم 🗣️", "ex_en": "We have the same opinion. 🤝", "ex_ar": "لدينا نفس الرأي."},
    "opinion": {"pron": "أُوبِينْيُوْن 🗣️", "ex_en": "In my opinion, you are right. 👍", "ex_ar": "في رأيي، أنت على حق."},
    "success": {"pron": "سَكْسِيسْ 🗣️", "ex_en": "Confidence is the key to success. 🔑", "ex_ar": "الثقة هي مفتاح النجاح."},
    "improve": {"pron": "إِمْبْرُوفْ 🗣️", "ex_en": "Practice every day to improve. 📖", "ex_ar": "تدرب كل يوم لتحسين مستواك."},
    "the": {"pron": "ذَا 🗣️", "ex_en": "The book is on the table. 📘", "ex_ar": "الكتاب على الطاولة."},
    "potato": {"pron": "بُوتِيتُو 🗣️", "ex_en": "I love eating fried potatoes! 🍟", "ex_ar": "أنا أحب أكل البطاطا المقلية!"}
}

# إنشاء الأزرار متوافقة مع شاشة الآيفون
def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar")
    btn2 = types.InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en")
    btn3 = types.InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart")
    keyboard.add(btn1, btn2, btn3)
    return keyboard

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_modes[message.chat.id] = 'smart_teacher'
    
    # إعداد زر القائمة الأزرق (Menu) أسفل الشاشة بشكل تلقائي ومضمون
    try:
        bot.set_my_commands([types.BotCommand("start", "🔄 الواجهة الرئيسية والاختيارات")])
    except Exception as e:
        pass

    welcome_text = (
        "✨ **مرحباً بك في بوت الترجمة الاحترافي الخارق** ✨\n"
        "👑 **بإشراف المطور قصي** 👑\n\n"
        "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي (نطق + أمثلة)_\n\n"
        "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# معالجة ضغطات الأزرار واختيار الوضع
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mode_en_to_ar":
        user_modes[call.message.chat.id] = 'en_to_ar'
        bot.send_message(call.message.chat.id, "🔄 **تم تفعيل الوضع:** [ إنجليزي ⬅️ عربي 🇵🇸 ]\n📥 أرسل لي أي كلمة أو جملة بالإنجليزية وسأترجمها فوراً!")
    elif call.data == "mode_ar_to_en":
        user_modes[call.message.chat.id] = 'ar_to_en'
        bot.send_message(call.message.chat.id, "🔄 **تم تفعيل الوضع:** [ عربي 🇵🇸 ⬅️ إنجليزي ]\n📥 أرسل لي أي كلمة أو جملة بالعربية وسأترجمها فوراً!")
    elif call.data == "mode_smart":
        user_modes[call.message.chat.id] = 'smart_teacher'
        bot.send_message(call.message.chat.id, "🧠 **تم تفعيل الوضع:** [ المعلم الذكي ]\n📥 أرسل الكلمة الإنجليزية لترى النطق بالعربي والأمثلة الكاملة!")
    bot.answer_callback_query(call.id)

# استقبال الرسائل (كلمات وجمل) وترجمتها فوراً
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text.strip()
    chat_id = message.chat.id
    current_mode = user_modes.get(chat_id, 'smart_teacher')
    
    # إرسال رسالة انتظار سريعة
    waiting_msg = bot.send_message(chat_id, "⏳ جاري الترجمة الاحترافية...")
    
    try:
        # 1️⃣ خيار: إنجليزي إلى عربي (جمل وكلمات)
        if current_mode == 'en_to_ar':
            translated = GoogleTranslator(source='en', target='ar').translate(user_text)
            res = f"🇺🇸 **النص الأصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة المباشرة:**\n*{translated}*"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        # 2️⃣ خيار: عربي إلى إنجليزي (جمل وكلمات)
        elif current_mode == 'ar_to_en':
            translated = GoogleTranslator(source='ar', target='en').translate(user_text)
            res = f"🇵🇸 **النص الأصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة المباشرة:**\n*{translated}*"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        # 3️⃣ خيار: المعلم الذكي
        elif current_mode == 'smart_teacher':
            # إذا كان المدخل كلمة واحدة بدون مسافات
            if " " not in user_text:
                word_clean = user_text.lower()
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                
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
                # إذا كانت جملة كاملة
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                response = (
                    f"📝 **تحليل الجملة الذكي:**\n\n"
                    f"🇺🇸 **الجملة الأصلية:** `{user_text}`\n"
                    f"🇵🇸 **ترجمتها الكاملة:** *{translated}*\n\n"
                    f"💡 _نصيحة المطور قصي:_ حاول تفكيك الجملة لحفظ الكلمات الفردية! 🚀"
                )
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
    except Exception as e:
        bot.edit_message_text("❌ عذراً، حدث خطأ أثناء الترجمة. حاول مجدداً!", chat_id, waiting_msg.message_id)

# تشغيل البوت
if __name__ == '__main__':
    print("البوت الجديد والآمن يعمل بنجاح وبدون أي كراش...")
    bot.infinity_polling()
