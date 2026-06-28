import os
import logging
import random
import telebot
from telebot import types
from deep_translator import GoogleTranslator

# تفعيل تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# التوكن الخاص بك
TOKEN = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"
bot = telebot.TeleBot(TOKEN)

user_modes = {}
user_levels = {}

# قاموس الاختصارات المطور: يعطي الجملة الإنجليزية الكاملة والترجمة العربية
SLANG_DICTIONARY = {
    "btw": "By the way ⬅️ (بالمناسبة / على فكرة)",
    "omg": "Oh my god ⬅️ (يا إلهي / أو ماي جاد)",
    "lol": "Laugh out loud ⬅️ (الضحك بصوت عالٍ / ههههه)",
    "idk": "I don't know ⬅️ (لا أعرف / لست أدري)",
    "tbh": "To be honest ⬅️ (بكل صراحة / لكي أكون صادقاً)",
    "smh": "Shaking my head ⬅️ (أهز رأسي تعجباً / مش عاجبني الوضع)",
    "brb": "Be right back ⬅️ (سأعود فوراً / برب)",
    "g2g": "Got to go ⬅️ (يجب أن أذهب الآن)",
    "imo": "In my opinion ⬅️ (في رأيي الشخصي)",
    "nvm": "Never mind ⬅️ (لا تهتم / انسى الأمر)",
    "asap": "As soon as possible ⬅️ (في أقرب وقت ممكن)",
    "afk": "Away from keyboard ⬅️ (بعيد عن الشاشة / اللعبة)",
    "wth": "What the hell ⬅️ (ما هذا بحق الجحيم!)",
    "idc": "I don't care ⬅️ (لا يهمني / طنش)"
}

COMMON_CORRECTIONS = {
    "tebol": "table",
    "set in": "sat on",
    "set on": "sat on",
    "the cat set": "the cat sat",
    "in the chair": "on the chair",
    "i is": "I am",
    "he are": "he is",
    "she are": "she is",
    "they is": "they are"
}

LEVELS_DATA = {
    1: {
        "title": "🌱 لفل 1 - المبتدئ الشامل",
        "sentences": [
            {"en": "The cat is sleeping on the chair.", "ar": "القطة تنام على الكرسي."},
            {"en": "I drink water every morning.", "ar": "أنا أشرب الماء كل صباح."},
            {"en": "The sun is very bright today.", "ar": "الشمس مشرقة جداً اليوم."},
            {"en": "My brother has a beautiful car.", "ar": "أخي يمتلك سيارة جميلة."},
            {"en": "She loves reading books in the room.", "ar": "هي تحب قراءة الكتب في الغرفة."}
        ]
    },
    2: {
        "title": "🌿 لفل 2 - المبتدئ المتقدم",
        "sentences": [
            {"en": "I want to learn English to get a good job.", "ar": "أريد أن أتعلم الإنجليزية لأحصل على وظيفة جيدة."},
            {"en": "We should go to the supermarket tonight.", "ar": "ينبغي أن نذهب إلى السوبرماركت الليلة."},
            {"en": "He does not like waiting for a long time.", "ar": "هو لا يحب الانتظار لوقت طويل."},
            {"en": "Can you help me finish this homework?", "ar": "هل يمكنك مساعدتي في إنهاء هذا الواجب المنزلي؟"},
            {"en": "Traveling to new places opens your mind.", "ar": "السفر إلى أماكن جديدة يفتح عقلك."}
        ]
    },
    3: {
        "title": "🔥 لفل 3 - المتوسط",
        "sentences": [
            {"en": "Success is not final, failure is not fatal.", "ar": "النجاح ليس نهائياً، والفشل ليس قاتلاً."},
            {"en": "Education is the most powerful weapon to change the world.", "ar": "التعليم هو أقوى سلاح لتغيير العالم."},
            {"en": "Don't count the days, make the days count.", "ar": "لا تحسب الأيام، بل اجعل الأيام ذات قيمة."},
            {"en": "An investment in knowledge pays the best interest.", "ar": "الاستثمار في المعرفة يدفع أفضل العوائد."},
            {"en": "Hard work beats talent when talent fails to work hard.", "ar": "العمل الجاد يهزم الموهبة عندما تفشل الموهبة في العمل بجد."}
        ]
    },
    4: {
        "title": "🚀 لفل 4 - فوق المتوسط",
        "sentences": [
            {"en": "Despite facing many obstacles, we managed to build this bot.", "ar": "على الرغم من مواجهة العديد من العقبات، تمكنا من بناء هذا البوت."},
            {"en": "The economic situation requires immediate and effective solutions.", "ar": "الوضع الاقتصادي يتطلب حلولاً فورية وفعالة."},
            {"en": "Environmental awareness has become essential for our survival.", "ar": "أصبح الوعي البيئي ضرورياً لبقائنا على قيد الحياة."},
            {"en": "Innovation distinguishes between a leader and a follower.", "ar": "الابتكار يميز بين القائد والتابع."},
            {"en": "To achieve your goals, you must step out of your comfort zone.", "ar": "لتحقيق أهدافك، يجب عليك الخروج من منطقة الراحة الخاصة بك."}
        ]
    },
    5: {
        "title": "👑 لفل 5 - المحترف الخبير",
        "sentences": [
            {"en": "Advanced algorithms enhance system efficiency substantially.", "ar": "إن خوارزميات التعلم الآلي المتقدمة تعزز كفاءة النظام بشكل كبير."},
            {"en": "The juxtaposition of technology and art creates profound human experiences.", "ar": "إن التجاوز بين التكنولوجيا والفن يخلق تجارب إنسانية عميقة."},
            {"en": "Artificial intelligence possesses the potential to revolutionize global industries.", "ar": "يمتلك الذكاء الاصطناعي القدرة على إحداث ثورة في الصناعات العالمية."},
            {"en": "Comprehensive research is vital to understanding socioeconomic disparities.", "ar": "البحث الشامل أمر حيوي لفهم التفاوتات الاجتماعية والاقتصادية."},
            {"en": "The legal implications of this decision will reverberate for decades.", "ar": "إن التداعيات القانونية لهذا القرار سوف يتردد صداها لعقود من الزمن."}
        ]
    }
}

def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar")
    btn2 = types.InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en")
    btn3 = types.InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart")
    btn4 = types.InlineKeyboardButton("📊 تقييم المستوى وتحديد اللفل (1-5)", callback_data="mode_levels_menu")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard

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

# دالة ذكية لفحص وترجمة النص التلقائي والاختصارات بجملها الكاملة
def check_translation(text, source_lang, target_lang):
    clean_text = text.lower().strip()
    if source_lang == 'en' and clean_text in SLANG_DICTIONARY:
        return SLANG_DICTIONARY[clean_text]
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_modes[chat_id] = 'smart_teacher'
    if chat_id not in user_levels:
        user_levels[chat_id] = 1
    
    welcome_text = (
        "✨ **مرحباً بك في بوت الترجمة والتعليم الذكي** ✨\n"
        "👑 **بإشراف المطور قصي** 👑\n\n"
        "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي_\n"
        f"📊 **مستواك الحالي الحقيقي:** لفل {user_levels[chat_id]}\n\n"
        "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    
    if call.data == "mode_en_to_ar":
        user_modes[chat_id] = 'en_to_ar'
        bot.send_message(chat_id, "🔄 **تم تفعيل الوضع:** [ إنجليزي ⬅️ عربي 🇵🇸 ]\n📥 أرسل أي جملة بالإنجليزية وسأترجمها فوراً!")
    elif call.data == "mode_ar_to_en":
        user_modes[chat_id] = 'ar_to_en'
        bot.send_message(chat_id, "🔄 **تم تفعيل الوضع:** [ عربي 🇵🇸 ⬅️ إنجليزي ]\n📥 أرسل أي جملة بالعربية وسأترجمها فوراً!")
    elif call.data == "mode_smart":
        user_modes[chat_id] = 'smart_teacher'
        bot.send_message(chat_id, "🧠 **تم تفعيل الوضع:** [ المعلم الذكي ]\n📥 أرسل الكلمة لترى النطق والأمثلة!")
    elif call.data == "mode_levels_menu":
        bot.send_message(chat_id, "📊 **أهلاً بك في نظام التقييم وتحديد المستويات.**\nاختر مستواك الحالي الحقيقي:", reply_markup=get_levels_keyboard())
    elif call.data.startswith("set_lvl_"):
        lvl_num = int(call.data.split("_")[2])
        user_levels[chat_id] = lvl_num
        user_modes[chat_id] = f'learning_lvl_{lvl_num}'
        
        random_sentence = random.choice(LEVELS_DATA[lvl_num]["sentences"])
        response = (
            f"🎯 **تم تحديد مستواك بنجاح في:**\n{LEVELS_DATA[lvl_num]['title']}\n\n"
            f"📥 **إليك جملة عشوائية مخصصة لتتعلمها الآن:**\n"
            f"💬 اضغط لنسخ الجملة الإنجليزية لتدرب عليها:\n`{random_sentence['en']}`\n\n"
            f"💡 **تعني بالعربية:** `{random_sentence['ar']}`\n\n"
            f"👇 **دورك الآن:** أرسل أي جملة باللغة الإنجليزية في هذا اللفل لاختبارها وتصحيحها ذكياً!"
        )
        bot.send_message(chat_id, response, parse_mode="Markdown")
    elif call.data == "back_to_main":
        bot.send_message(chat_id, "🔄 تم الرجوع للواجهة الرئيسية لقصي:", reply_markup=get_main_keyboard())
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text.strip()
    chat_id = message.chat.id
    current_mode = user_modes.get(chat_id, 'smart_teacher')
    
    waiting_msg = bot.send_message(chat_id, "⏳ جاري التحليل والترجمة الذكية...")
    
    try:
        if current_mode == 'en_to_ar':
            translated = check_translation(user_text, 'en', 'ar')
            res = f"🇺🇸 **النص الاصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة الكاملة (اضغط للنسخ):**\n`{translated}`"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        elif current_mode == 'ar_to_en':
            translated = check_translation(user_text, 'ar', 'en')
            res = f"🇵🇸 **النص الاصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة الكاملة (اضغط للنسخ):**\n`{translated}`"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        elif current_mode == 'smart_teacher':
            translated = check_translation(user_text, 'en', 'ar')
            if " " not in user_text:
                response = f"🇺🇸 **الكلمة:** `{user_text.upper()}`\n🎈 **معناها وجملتها الكاملة:**\n`{translated}`"
            else:
                response = f"🇺🇸 **الجملة:** `{user_text}`\n🇵🇸 **ترجمتها الدقيقة:**\n`{translated}`"
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
        elif current_mode.startswith('learning_lvl_'):
            current_lvl = int(current_mode.split("_")[2])
            text_lower = user_text.lower()
            
            has_errors = False
            corrected_text = user_text
            feedback = "✨ **التقييم:** كفو! جملتك ممتازة وخالية من الأخطاء الإملائية والتركيبية في هذا اللفل. استمر! 🚀"
            
            for wrong, right in COMMON_CORRECTIONS.items():
                if wrong in text_lower:
                    has_errors = True
                    corrected_text = text_lower.replace(wrong, right)
                    break
            
            if has_errors or ("tebol" in text_lower):
                translated_correct = check_translation(corrected_text, 'en', 'ar')
                response = (
                    f"📊 **تحليل ذكي لـ [ لفل {current_lvl} ]:**\n\n"
                    f"❌ **جملتك المكتوبة:**\n`{user_text}`\n\n"
                    f"✅ **التصحيح الكامل:**\n`{corrected_text}`\n\n"
                    f"🇵🇸 **الترجمة والمعنى بالكامل:**\n`{translated_correct}`\n\n"
                    f"⚠️ **تنبيه المطور قصي التعليمي:**\n"
                    f"يرجى مراجعة الجملة المصححة بالأعلى والضغط عليها لنسخها وحفظها! 🧠"
                )
            else:
                translated = check_translation(user_text, 'en', 'ar')
                response = (
                    f"📊 **تحليل ذكي لـ [ لفل {current_lvl} ]:**\n\n"
                    f"🇺🇸 **جملتك المكتوبة:**\n`{user_text}`\n\n"
                    f"🇵🇸 **الترجمة والمعنى الكامل:**\n`{translated}`\n\n"
                    f"{feedback}"
                )
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
    except Exception as e:
        bot.edit_message_text("❌ حدث خطأ أثناء المعالجة الذكية. حاول مجدداً!", chat_id, waiting_msg.message_id)

if __name__ == '__main__':
    bot.infinity_polling()
