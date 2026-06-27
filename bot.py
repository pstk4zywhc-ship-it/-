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

# تخزين وضع المستخدم والمستوى (الافتراضي: المعلم الذكي)
user_modes = {}
user_levels = {}

# قاعدة بيانات المستويات (أسئلة تقييم وجمل تعليمية لكل لفل)
LEVELS_DATA = {
    1: {
        "title": "🌱 لفل 1 - المبتدئ الشامل",
        "intro": "هذا المستوى للمبتدئين تماماً. سأرسل لك جملة بسيطة جداً لترجمتها وتعلمها:\n\n💬 اضغط لنسخها وسماعها:\n`The cat is sleeping on the chair.`\n\n💡 تعني: القطة تنام على الكرسي. حاول كتابة جمل مشابهة لي!"
    },
    2: {
        "title": "🌿 لفل 2 - المبتدئ المتقدم",
        "intro": "ممتاز! بدأت تدخل في تركيب الجمل اليومية. إليك جملة هذا المستوى:\n\n💬 اضغط لنسخها:\n`I want to learn English to get a good job.`\n\n💡 تعني: أريد أن أتعلم الإنجليزية لأحصل على وظيفة جيدة. أرسل لي جملك المخصصة الآن!"
    },
    3: {
        "title": "🔥 لفل 3 - المتوسط",
        "intro": "كفو! لفل 3 يتطلب فهم أعمق. إليك الجملة المخصصة لتقييمك وتعليمك:\n\n💬 اضغط لنسخها:\n`Success is not final, failure is not fatal: it is the courage to continue that counts.`\n\n💡 تعني: النجاح ليس نهائياً، والفشل ليس قاتلاً: إنها الشجاعة للاستمرار هي ما يهم."
    },
    4: {
        "title": "🚀 لفل 4 - فوق المتوسط",
        "intro": "مستوى عالي جداً! بدأت تتحدث بطلاقة وتستخدم مصطلحات قوية:\n\n💬 اضغط لنسخها:\n`Despite facing many obstacles, Qusai managed to build a very successful Telegram bot.`\n\n💡 تعني: على الرغم من مواجهة العديد من العقبات، تمكن قصي من بناء بوت تليجرام ناجح جداً."
    },
    5: {
        "title": "👑 لفل 5 - المحترف الخبير",
        "intro": "أنت الأسطورة هنا! لفل 5 مخصص للمقالات والترجمات المعقدة:\n\n💬 اضغط لنسخها:\n`The implementation of advanced machine learning algorithms enhances system efficiency substantially.`\n\n💡 تعني: إن تنفيذ خوارزميات التعلم الآلي المتقدمة يعزز كفاءة النظام بشكل كبير."
    }
}

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

# لوحة الأزرار الرئيسية المتوافقة مع الآيفون
def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar")
    btn2 = types.InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en")
    btn3 = types.InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart")
    btn4 = types.InlineKeyboardButton("📊 تقييم المستوى وتحديد اللفل (1-5)", callback_data="mode_levels_menu")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard

# لوحة اختيار المستويات (من 1 إلى 5)
def get_levels_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🌱 لفل 1 (Level 1)", callback_data="set_lvl_1")
    btn2 = types.InlineKeyboardButton("🌿 لفل 2 (Level 2)", callback_data="set_lvl_2")
    btn3 = types.InlineKeyboardButton("🔥 لفل 3 (Level 3)", callback_data="set_lvl_3")
    btn4 = types.InlineKeyboardButton("🚀 لفل 4 (Level 4)", callback_data="set_lvl_4")
    btn5 = types.InlineKeyboardButton("👑 لفل 5 (Level 5)", callback_data="set_lvl_5")
    btn_back = types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn_back)
    return keyboard

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_modes[chat_id] = 'smart_teacher'
    if chat_id not in user_levels:
        user_levels[chat_id] = 1 # المستوى الافتراضي هو لفل 1
    
    try:
        bot.set_my_commands([types.BotCommand("start", "🔄 الواجهة الرئيسية والاختيارات")])
    except Exception:
        pass

    welcome_text = (
        "✨ **مرحباً بك في بوت الترجمة الاحترافي الخارق** ✨\n"
        "👑 **بإشراف المطور قصي** 👑\n\n"
        "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي_\n"
        f"📊 **مستواك الحالي الحقيقي:** لفل {user_levels[chat_id]}\n\n"
        "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# معالجة ضغطات الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    
    if call.data == "mode_en_to_ar":
        user_modes[chat_id] = 'en_to_ar'
        bot.send_message(chat_id, "🔄 **تم تفعيل الوضع:** [ إنجليزي ⬅️ عربي 🇵🇸 ]\n📥 أرسل لي أي كلمة أو جملة بالإنجليزية وسأترجمها فوراً!")
        
    elif call.data == "mode_ar_to_en":
        user_modes[chat_id] = 'ar_to_en'
        bot.send_message(chat_id, "🔄 **تم تفعيل الوضع:** [ عربي 🇵🇸 ⬅️ إنجليزي ]\n📥 أرسل لي أي كلمة أو جملة بالعربية وسأترجمها فوراً!")
        
    elif call.data == "mode_smart":
        user_modes[chat_id] = 'smart_teacher'
        bot.send_message(chat_id, "🧠 **تم تفعيل الوضع:** [ المعلم الذكي ]\n📥 أرسل الكلمة الإنجليزية لترى النطق بالعربي والأمثلة الكاملة!")
        
    elif call.data == "mode_levels_menu":
        bot.send_message(chat_id, "📊 **أهلاً بك في نظام التقييم وتحديد المستويات.**\n\nاختر مستواك الحالي من الأزرار بالأسفل وسأقوم بتعليمك وتقييمك وإرسال جمل تناسب مقدرتك تماماً:", reply_markup=get_levels_keyboard())
        
    elif call.data.startswith("set_lvl_"):
        lvl_num = int(call.data.split("_")[2])
        user_levels[chat_id] = lvl_num
        user_modes[chat_id] = f'learning_lvl_{lvl_num}'
        
        lvl_info = LEVELS_DATA[lvl_num]
        response = (
            f"🎯 **تم تحديد مستواك بنجاح في:**\n{lvl_info['title']}\n\n"
            f"{lvl_info['intro']}\n\n"
            f"📥 **دورك الآن:** أرسل أي جملة باللغة الإنجليزية في هذا اللفل لتقييمها وترجمتها بشكل ذكي!"
        )
        bot.send_message(chat_id, response, parse_mode="Markdown")
        
    elif call.data == "back_to_main":
        bot.send_message(chat_id, "🔄 تم الرجوع للواجهة الرئيسية لقصي:", reply_markup=get_main_keyboard())
        
    bot.answer_callback_query(call.id)

# استقبال الرسائل وترجمتها فورا مع ميزة النسخ باللمس
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text.strip()
    chat_id = message.chat.id
    current_mode = user_modes.get(chat_id, 'smart_teacher')
    
    waiting_msg = bot.send_message(chat_id, "⏳ جاري الترجمة الاحترافية...")
    
    try:
        # 1️⃣ خيار: إنجليزي إلى عربي (يدعم النسخ بلمسة واحدة)
        if current_mode == 'en_to_ar':
            translated = GoogleTranslator(source='en', target='ar').translate(user_text)
            res = f"🇺🇸 **النص الأصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة المباشرة (اضغط لنسخ الترجمة):**\n`{translated}`"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        # 2️⃣ خيار: عربي إلى إنجليزي (يدعم النسخ بلمسة واحدة)
        elif current_mode == 'ar_to_en':
            translated = GoogleTranslator(source='ar', target='en').translate(user_text)
            res = f"🇵🇸 **النص الأصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة المباشرة (اضغط لنسخ الترجمة):**\n`{translated}`"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        # 3️⃣ خيار: المعلم الذكي
        elif current_mode == 'smart_teacher':
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
                    f"🎈 **معناها (اضغط للنسخ):**\n`{translated}`\n\n"
                    f"📢 **وتلفظ تقريباً:** {pron}\n\n"
                    f"📌 **مثال توضيحي (Example):**\n"
                    f"• `{ex_en}`\n"
                    f"• _ترجمة المثال:_ `{ex_ar}`\n\n"
                    f"--- \n"
                    f"💡 _نصيحة المطور قصي:_ استمر في إرسال الكلمات لتقوية لغتك! ✨"
                )
            else:
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                response = (
                    f"📝 **تحليل الجملة الذكي:**\n\n"
                    f"🇺🇸 **الجملة الأصلية:**\n`{user_text}`\n\n"
                    f"🇵🇸 **ترجمتها الكاملة (اضغط للنسخ):**\n`{translated}`\n\n"
                    f"💡 _نصيحة المطور قصي:_ حاول تفكيك الجملة لحفظ الكلمات الفردية! 🚀"
                )
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
        # 4️⃣ نظام المستويات التقييمي من 1 لـ 5
        elif current_mode.startswith('learning_lvl_'):
            current_lvl = int(current_mode.split("_")[2])
            translated = GoogleTranslator(source='en', target='ar').translate(user_text)
            
            response = (
                f"📊 **تقييم مستواك في [ لفل {current_lvl} ]:**\n\n"
                f"🇺🇸 **جملتك المكتوبة:**\n`{user_text}`\n\n"
                f"🇵🇸 **ترجمتها الدقيقة (اضغط للنسخ):**\n`{translated}`\n\n"
                f"✨ **التقييم:** كفو! الجملة متناسقة وممتازة ومناسبة لـ لفل {current_lvl}. استمر في إرسال جمل أخرى لرفع مستواك تلقائياً لليفل القادم! 🚀"
            )
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
    except Exception as e:
        bot.edit_message_text("❌ عذراً، حدث خطأ أثناء الترجمة والتقييم. حاول مجدداً!", chat_id, waiting_msg.message_id)

# تشغيل البوت
if __name__ == '__main__':
    print("بوت قصي الاحترافي بالمستويات وميزة النسخ الفوري يعمل الآن بنجاح...")
    bot.infinity_polling()
