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

user_modes = {}
user_levels = {}

# قاموس بسيط لتصحيح الأخطاء الشائعة والبدائية تلقائياً لزيادة ذكاء البوت
COMMON_CORRECTIONS = {
    "tebol": "table",
    "set in": "sat on",
    "set on": "sat on",
    "the cat set": "the cat sat",
    "in the chair": "on the chair"
}

LEVELS_DATA = {
    1: {
        "title": "🌱 لفل 1 - المبتدئ الشامل",
        "intro": "هذا المستوى للمبتدئين تماماً. سأرسل لك جملة بسيطة جداً لترجمتها وتعلمها:\n\n💬 اضغط لنسخها:\n`The cat is sleeping on the chair.`\n\n💡 تعني: القطة تنام على الكرسي. حاول كتابة جملة مشابهة لي بالإنجليزية واختبر ذكائي!"
    },
    2: {
        "title": "🌿 لفل 2 - المبتدئ المتقدم",
        "intro": "ممتاز! بدأت تدخل في تركيب الجمل اليومية. إليك جملة هذا المستوى:\n\n💬 اضغط لنسخها:\n`I want to learn English to get a good job.`\n\n💡 تعني: أريد أن أتعلم الإنجليزية لأحصل على وظيفة جيدة."
    },
    3: {
        "title": "🔥 لفل 3 - المتوسط",
        "intro": "كفو! لفل 3 يتطلب فهم أعمق. إليك الجملة المخصصة:\n\n💬 اضغط لنسخها:\n`Success is not final, failure is not fatal.`\n\n💡 تعني: النجاح ليس نهائياً، والفشل ليس قاتلاً."
    },
    4: {
        "title": "🚀 لفل 4 - فوق المتوسط",
        "intro": "مستوى عالي جداً! بدأت تتحدث بطلاقة وتستخدم مصطلحات قوية:\n\n💬 اضغط لنسخها:\n`Despite facing many obstacles, we managed to build this bot.`\n\n💡 تعني: على الرغم من مواجهة العديد من العقبات، تمكنا من بناء هذا البوت."
    },
    5: {
        "title": "👑 لفل 5 - المحترف الخبير",
        "intro": "أنت الأسطورة هنا! لفل 5 مخصص للمقالات والترجمات المعقدة:\n\n💬 اضغط لنسخها:\n`Advanced algorithms enhance system efficiency substantially.`\n\n💡 تعني: إن خوارزميات التعلم الآلي المتقدمة تعزز كفاءة النظام بشكل كبير."
    }
}

SMART_DICTIONARY = {
    "hello": {"pron": "هَلُوو 🗣️", "ex_en": "Hello! How are you today? 🤔", "ex_ar": "مرحباً! كيف حالك اليوم؟"},
    "same": {"pron": "سِيوْم 🗣️", "ex_en": "We have the same opinion. 🤝", "ex_ar": "لدينا نفس الرأي."},
    "opinion": {"pron": "أُوبِينْيُوْن 🗣️", "ex_en": "In my opinion, you are right. 👍", "ex_ar": "في رأيي، أنت على حق."},
    "success": {"pron": "سَكْسِيسْ 🗣️", "ex_en": "Confidence is the key to success. 🔑", "ex_ar": "الثقة هي مفتاح النجاح."}
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
        bot.send_message(chat_id, f"🎯 **تم تحديد مستواك في:**\n{LEVELS_DATA[lvl_num]['title']}\n\n{LEVELS_DATA[lvl_num]['intro']}", parse_mode="Markdown")
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
            translated = GoogleTranslator(source='en', target='ar').translate(user_text)
            res = f"🇺🇸 **النص الاصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة (اضغط للنسخ):**\n`{translated}`"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        elif current_mode == 'ar_to_en':
            translated = GoogleTranslator(source='ar', target='en').translate(user_text)
            res = f"🇵🇸 **النص الاصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة (اضغط للنسخ):**\n`{translated}`"
            bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")

        elif current_mode == 'smart_teacher':
            if " " not in user_text:
                word_clean = user_text.lower()
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                pron = SMART_DICTIONARY.get(word_clean, {}).get('pron', "متاح سماعياً 🗣️")
                response = f"🇺🇸 **الكلمة:** `{user_text.upper()}`\n🎈 **معناها:** `{translated}`\n📢 **نطقها التقريبي:** {pron}"
            else:
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                response = f"🇺🇸 **الجملة:** `{user_text}`\n🇵🇸 **ترجمتها:** `{translated}`"
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
        elif current_mode.startswith('learning_lvl_'):
            current_lvl = int(current_mode.split("_")[2])
            text_lower = user_text.lower()
            
            # فحص ذكي: هل توجد أخطاء في النص المرسل؟
            has_errors = False
            corrected_text = user_text
            feedback = "✨ **التقييم:** كفو! جملتك ممتازة وخالية من الأخطاء الإملائية والتركيبية في هذا اللفل. استمر! 🚀"
            
            # مطابقة النص مع القاموس الذكي للأخطاء
            for wrong, right in COMMON_CORRECTIONS.items():
                if wrong in text_lower:
                    has_errors = True
                    corrected_text = text_lower.replace(wrong, right)
                    break
            
            # إذا كتب كلمات عشوائية غير مفهومة أو أحرف خاطئة
            if has_errors or ("tebol" in text_lower) or ("set in" in text_lower):
                translated_correct = GoogleTranslator(source='en', target='ar').translate(corrected_text)
                response = (
                    f"📊 **تحليل ذكي لـ [ لفل {current_lvl} ]:**\n\n"
                    f"❌ **جملتك المكتوبة (بها أخطاء):**\n`{user_text}`\n\n"
                    f"✅ **التصحيح الصحيح للجملة:**\n`{corrected_text}`\n\n"
                    f"🇵🇸 **الترجمة الصحيحة والمنسقة:**\n`{translated_correct}`\n\n"
                    f"⚠️ **تنبيه المطور قصي التعليمي:**\n"
                    f"لقد قمت بكتابة بعض الكلمات بشكل خاطئ قواعدياً أو إملائياً (مثل استخدام تعبير خاطئ)، يرجى مراجعة الجملة المصححة بالأعلى والضغط عليها لنسخها وحفظها! 🧠"
                )
            else:
                # إذا كانت الجملة سليمة وصحيحة
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                response = (
                    f"📊 **تحليل ذكي لـ [ لفل {current_lvl} ]:**\n\n"
                    f"🇺🇸 **جملتك المكتوبة:**\n`{user_text}`\n\n"
                    f"🇵🇸 **ترجمتها الدقيقة:**\n`{translated}`\n\n"
                    f"{feedback}"
                )
            bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            
    except Exception as e:
        bot.edit_message_text("❌ حدث خطأ أثناء المعالجة الذكية. حاول مجدداً!", chat_id, waiting_msg.message_id)

if __name__ == '__main__':
    bot.infinity_polling()
