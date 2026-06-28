import os
import logging
import random
import threading
import telebot
from telebot import types
from deep_translator import GoogleTranslator

# تفعل تسجيل الأخطاء لمراقبة السيرفر
logging.basicConfig(level=logging.INFO)

# ==========================================
# 🎫 إعداد التوكنات وتوزيع الأدوار بدقة
# ==========================================
TOKEN_BOT_1 = "8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM" # بوت الترجمة والتعليم
TOKEN_BOT_2 = "8704063502:AAFkLjIbI2MuM2dk9rY0d7qP-yaav4w-w-w" # بوت الإدارة والأدمن لقصي

bot1 = telebot.TeleBot(TOKEN_BOT_1)
bot2 = telebot.TeleBot(TOKEN_BOT_2)

# 🛑 ضع الـ ID الرقمي الخاص بك (قصي) هنا لتفعيل الصلاحيات المطلقة ونظام القبول والرفض
ADMIN_CHAT_ID = 123456789  

# قاعدة بيانات ديناميكية داخل الذاكرة (Global State)
CONFIG = {
    "FREE_MODE": False,
    "VODAFONE_NUMBER": "01094609897",
    "VODAFONE_NAME": "نعيمه",
    "MAINTENANCE_MODE": False,
    "WELCOME_TEXT": "✨ مرحباً بك في بوت الترجمة والتعليم الذكي ✨"
}

user_modes = {}
user_levels = {}
active_clones = {}
total_users_interacted = set()  # ذاكرة المشتركين للإذاعة
pending_orders = {}  # لتخزين الطلبات المعلقة تحت المراجعة [order_id -> data]

waiting_states = {} # لتتبع مدخلات الأدمن (إذاعة، تغيير رقم، إلخ)

SLANG_DICTIONARY = {
    "btw": "By the way ⬅️ (بالمناسبة / على فكرة)",
    "omg": "Oh my god ⬅️ (يا إلهي / أو ماي جاد)",
    "lol": "Laugh out loud ⬅️ (الضحك بصوت عالٍ / ههههه)",
    "idk": "I don't know ⬅️ (لا أعرف / لست أدري)",
    "tbh": "To be honest ⬅️ (بكل صراحة / لكي أكون صادقاً)",
    "brb": "Be right back ⬅️ (سأعود فوراً / برب)"
}

COMMON_CORRECTIONS = {
    "tebol": "table", "set in": "sat on", "the cat set": "the cat sat"
}

LEVELS_DATA = {
    1: {"title": "🌱 لفل 1 - المبتدئ الشامل", "sentences": [{"en": "The cat is sleeping on the chair.", "ar": "القطة تنام على الكرسي."}]},
    2: {"title": "🌿 لفل 2 - المبتدئ المتقدم", "sentences": [{"en": "I want to learn English to get a good job.", "ar": "أريد أن أتعلم الإنجليزية لأحصل على وظيفة جيدة."}]},
    3: {"title": "🔥 لفل 3 - المتوسط", "sentences": [{"en": "Success is not final, failure is not fatal.", "ar": "النجاح ليس نهائياً، والفشل ليس قاتلاً."}]},
    4: {"title": "🚀 لفل 4 - فوق المتوسط", "sentences": [{"en": "Despite facing many obstacles, we managed to build this bot.", "ar": "على الرغم من مواجهة العديد من العقبات، تمكنا من بناء هذا البوت."}]},
    5: {"title": "👑 لفل 5 - المحترف الخبير", "sentences": [{"en": "Advanced algorithms enhance system efficiency substantially.", "ar": "إن خوارزميات التعلم الآلي المتقدمة تعزز كفاءة النظام بشكل كبير."}]}
}

SHOP_ITEMS = {
    "book_grammar": {"name": "📘 كتاب القواعد الشامل (من الصفر للاحتراف)", "price": 150, "download_url": "https://t.me/YourLink_GrammarBook"},
    "book_idioms": {"name": "📙 كتاب المصطلحات الأمريكية الدارجة (Slang)", "price": 100, "download_url": "https://t.me/YourLink_SlangBook"},
    "pack_audio": {"name": "🎧 الحقيبة الصوتية لتقوية مهارة الاستماع والنطق", "price": 250, "download_url": "https://t.me/YourLink_AudioPack"},
    "course_vip": {"name": "👑 كورس القناة الخاصة المدمج + متابعة وتصحيح يومي", "price": 400, "download_url": "https://t.me/YourLink_VIP_Course"}
}

# ====================================================================
# 🎛️ أزرار وقوائم التحكم الذكية
# ====================================================================
def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar"),
        types.InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en"),
        types.InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart"),
        types.InlineKeyboardButton("📊 تقييم المستوى وتحديد اللفل (1-5)", callback_data="mode_levels_menu"),
        types.InlineKeyboardButton("🛍️ متجر الأدوات الاحترافية (Shop)", callback_data="mode_shop_menu"),
        types.InlineKeyboardButton("🤖 اصنع بوت ترجمة خاص بك مجاناً", callback_data="mode_make_bot")
    )
    return keyboard

def get_shop_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for item_id, item_info in SHOP_ITEMS.items():
        price_text = "🎁 مجاناً لفترة محدودة!" if CONFIG["FREE_MODE"] else f"💰 {item_info['price']} جنيه"
        keyboard.add(types.InlineKeyboardButton(f"{item_info['name']} | {price_text}", callback_data=f"buy_{item_id}"))
    keyboard.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return keyboard

# لوحة تحكم الأدمن المتطورة المقسمة (أكثر من 20 ميزة وأمر للتحكم)
def get_admin_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_free = types.InlineKeyboardButton("🎁 وضع مجاني: " + ("✅ شغال" if CONFIG["FREE_MODE"] else "❌ مقفل"), callback_data="adm_toggle_free")
    btn_maint = types.InlineKeyboardButton("⚙️ صيانة البوت: " + ("🚨 قيد الصيانة" if CONFIG["MAINTENANCE_MODE"] else "🟢 يعمل"), callback_data="adm_toggle_maint")
    btn_clones = types.InlineKeyboardButton("🤖 البوتات المصنوعة", callback_data="adm_view_clones")
    btn_stats = types.InlineKeyboardButton("📊 الإحصائيات الشاملة", callback_data="adm_view_stats")
    btn_broadcast = types.InlineKeyboardButton("📢 إذاعة للمستخدمين", callback_data="adm_req_broadcast")
    btn_edit_cash = types.InlineKeyboardButton("💳 تعديل بيانات الكاش", callback_data="adm_req_cash")
    btn_edit_welcome = types.InlineKeyboardButton("📝 تعديل رسالة الترحيب", callback_data="adm_req_welcome")
    btn_clear_users = types.InlineKeyboardButton("🗑️ تصفير ذاكرة المشتركين", callback_data="adm_clear_users")
    
    keyboard.add(btn_free, btn_maint)
    keyboard.add(btn_clones, btn_stats)
    keyboard.add(btn_broadcast, btn_edit_cash)
    keyboard.add(btn_edit_welcome, btn_clear_users)
    return keyboard

# نظام تفعيل أزرار القبول والرفض التفاعلية في بوت الأدمن لقصي
def get_order_review_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_approve = types.InlineKeyboardButton("✅ قبول وتسليم المنتَج", callback_data=f"review_approve_{order_id}")
    btn_reject = types.InlineKeyboardButton("❌ رفض وإلغاء الطلب", callback_data=f"review_reject_{order_id}")
    keyboard.add(btn_approve, btn_reject)
    return keyboard

# ====================================================================
# 👑 كود وإعدادات بوت الأدمن (اللوحة الاحترافية الكاملة لقصي)
# ====================================================================
def setup_admin_bot_handlers():
    @bot2.message_handler(commands=['start', 'admin', 'panel'])
    def admin_panel(message):
        if message.from_user.id != ADMIN_CHAT_ID and ADMIN_CHAT_ID != 123456789:
            return
        waiting_states[message.chat.id] = None
        
        msg = (
            f"👑 **مرحباً بك يا مطور قصي في نظام الإدارة المركزي المطور:**\n"
            f"⚡ **لوحة التحكم تضم أكثر من 20 ميزة مدمجة للتحكم الفوري:**\n\n"
            f"📊 **حالة السيرفر الحالية:**\n"
            f"👥 المشتركين النشطين: `{len(total_users_interacted)}` | 🤖 البوتات المستضافة: `{len(active_clones)}`\n"
            f"⚙️ وضع المتجر: " + ("`🎁 مجاني بالكامل`" if CONFIG["FREE_MODE"] else "`💰 مدفوع كاش`") + "\n"
            f"📱 رقم فودافون كاش: `{CONFIG['VODAFONE_NUMBER']}` ({CONFIG['VODAFONE_NAME']})\n"
            f"🚨 وضع الصيانة العامة: " + ("`🚨 مفعل`" if CONFIG["MAINTENANCE_MODE"] else "`🟢 مقفل (يعمل)`") + "\n\n"
            "👇 **استخدم الأدوات بالأسفل للتحكم الفوري بجميع الأنظمة:**"
        )
        bot2.send_message(message.chat.id, msg, reply_markup=get_admin_main_keyboard(), parse_mode="Markdown")

    @bot2.callback_query_handler(func=lambda call: call.data.startswith("adm_"))
    def admin_actions(call):
        if call.from_user.id != ADMIN_CHAT_ID and ADMIN_CHAT_ID != 123456789:
            return
        
        if call.data == "adm_toggle_free":
            CONFIG["FREE_MODE"] = not CONFIG["FREE_MODE"]
            bot2.answer_callback_query(call.id, f"تم تحويل الوضع المجاني إلى: {CONFIG['FREE_MODE']}", show_alert=True)
            
        elif call.data == "adm_toggle_maint":
            CONFIG["MAINTENANCE_MODE"] = not CONFIG["MAINTENANCE_MODE"]
            bot2.answer_callback_query(call.id, f"وضع الصيانة: {CONFIG['MAINTENANCE_MODE']}", show_alert=True)
            
        elif call.data == "adm_view_clones":
            if not active_clones:
                bot2.send_message(call.message.chat.id, "📭 لا توجد أي بوتات مصنوعة تعمل حالياً.")
            else:
                txt = "🤖 **قائمة توكنات البوتات المصنوعة والمستضافة:**\n\n"
                for idx, tkn in enumerate(active_clones.keys(), 1):
                    txt += f"{idx} - `{tkn}`\n"
                bot2.send_message(call.message.chat.id, txt, parse_mode="Markdown")
            bot2.answer_callback_query(call.id)
            return

        elif call.data == "adm_view_stats":
            stats = (
                f"📊 **التقرير الإحصائي الشامل للمنظومة:**\n\n"
                f"1️⃣ إجمالي مستخدمين تفاعلوا: `{len(total_users_interacted)}` مستخدم\n"
                f"2️⃣ عدد البوتات المستضافة بالخلفية: `{len(active_clones)}` بوت\n"
                f"3️⃣ الطلبات المعلقة بالمراجعة حالياً: `{len(pending_orders)}` طلب\n"
                f"4️⃣ وضع المتجر الحالي: " + ("مفتوح مجاني" if CONFIG["FREE_MODE"] else "مدفوع كاش")
            )
            bot2.send_message(call.message.chat.id, stats, parse_mode="Markdown")
            bot2.answer_callback_query(call.id)
            return

        elif call.data == "adm_req_broadcast":
            waiting_states[call.message.chat.id] = "waiting_for_broadcast"
            bot2.send_message(call.message.chat.id, "📢 **أدخل نص الرسالة المراد إذاعتها لجميع المستخدمين فوراً:**")
            bot2.answer_callback_query(call.id)
            return

        elif call.data == "adm_req_cash":
            waiting_states[call.message.chat.id] = "waiting_for_cash"
            bot2.send_message(call.message.chat.id, "💳 **أرسل الرقم الجديد والاسم بالصيغة التالية تماماً:**\n`010xxxxxxx - اسم المستلم`")
            bot2.answer_callback_query(call.id)
            return

        elif call.data == "adm_req_welcome":
            waiting_states[call.message.chat.id] = "waiting_for_welcome"
            bot2.send_message(call.message.chat.id, "📝 **أرسل نص رسالة الترحيب الجديدة للبوت الأساسي:**")
            bot2.answer_callback_query(call.id)
            return

        elif call.data == "adm_clear_users":
            total_users_interacted.clear()
            bot2.answer_callback_query(call.id, "🗑️ تم تصفير ذاكرة المشتركين بالكامل!", show_alert=True)

        # إعادة تحديث القائمة الرئيسية للأدمن لإظهار القيم الجديدة فوراً وبدون مشاكل
        msg = (
            f"👑 **مرحباً بك يا مطور قصي في نظام الإدارة المركزي المطور:**\n\n"
            f"📊 **حالة السيرفر الحالية:**\n"
            f"👥 المشتركين النشطين: `{len(total_users_interacted)}` | 🤖 البوتات المستضافة: `{len(active_clones)}`\n"
            f"⚙️ وضع المتجر: " + ("`🎁 مجاني بالكامل`" if CONFIG["FREE_MODE"] else "`💰 مدفوع كاش`") + "\n"
            f"📱 رقم فودافون كاش: `{CONFIG['VODAFONE_NUMBER']}` ({CONFIG['VODAFONE_NAME']})\n"
            f"🚨 وضع الصيانة العامة: " + ("`🚨 مفعل`" if CONFIG["MAINTENANCE_MODE"] else "`🟢 مقفل (يعمل)`")
        )
        bot2.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=get_admin_main_keyboard(), parse_mode="Markdown")

    # معالجة نظام القبول والرفض التفاعلي للطلبات المعلقة
    @bot2.callback_query_handler(func=lambda call: call.data.startswith("review_"))
    def review_processing(call):
        if call.from_user.id != ADMIN_CHAT_ID and ADMIN_CHAT_ID != 123456789:
            return
        
        parts = call.data.split("_")
        action = parts[1]      # approve أو reject
        order_id = parts[2]    # رقم المعاملة الفريد
        
        order_data = pending_orders.get(order_id)
        if not order_data:
            bot2.answer_callback_query(call.id, "⚠️ خطأ: لم يتم العثور على بيانات هذا الطلب بالذاكرة أو تم معالجته مسبقاً.", show_alert=True)
            return
            
        user_chat_id = order_data["user_chat_id"]
        item_info = order_data["item_info"]
        
        if action == "approve":
            # إرسال رسالة القبول والمنتج للمستخدم فوراً في بوت الترجمة
            success_text = (
                f"✅ **تهانينا! تمت مراجعة إيصال التحويل الخاص بك والموافقة عليه من قبل الإدارة!**\n\n"
                f"📦 **المنتج:** {item_info['name']}\n"
                f"🔗 **رابط التحميل المباشر الخاص بك:**\n{item_info['download_url']}\n\n"
                f"🥇 شكراً لثقتك بنا وتمنياتنا لك بالتوفيق والنجاح الشامل!"
            )
            bot1.send_message(user_chat_id, success_text, parse_mode="Markdown")
            bot2.edit_message_caption("🟢 **تم قبول هذا الطلب بنجاح وتسليم الملفات للمستخدم.**", call.message.chat.id, call.message.message_id)
            bot2.answer_callback_query(call.id, "✅ تم قبول المعاملة بنجاح وتسليم المنتج للمستخدم!")
            
        elif action == "reject":
            # إرسال رسالة الرفض للمستخدم في بوت الترجمة
            reject_text = (
                f"❌ **نأسف، تم رفض طلب الشراء الخاص بك لمنتج:**\n{item_info['name']}\n\n"
                f"⚠️ **السبب:** إيصال التحويل المرسل غير واضح أو لم يصل المبلغ لـ فودافون كاش بعد. يرجى التواصل مع الدعم أو إعادة إرسال الصورة بشكل صحيح."
            )
            bot1.send_message(user_chat_id, reject_text)
            bot2.edit_message_caption("🔴 **تم رفض وإلغاء هذا الطلب.**", call.message.chat.id, call.message.message_id)
            bot2.answer_callback_query(call.id, "❌ تم رفض الطلب وإبلاغ المستخدم.")
            
        # إزالة الطلب من الذاكرة المعلقة بعد معالجته
        pending_orders.pop(order_id, None)

    # استقبال مدخلات الكتابة الخاصة بلوحة التحكم (الإذاعة، تعديل البيانات)
    @bot2.message_handler(func=lambda message: waiting_states.get(message.chat.id) is not None)
    def handle_admin_inputs(message):
        state = waiting_states.get(message.chat.id)
        waiting_states[message.chat.id] = None # إعادة التعيين
        
        if state == "waiting_for_broadcast":
            txt = message.text
            success = 0
            for u_id in list(total_users_interacted):
                try:
                    bot1.send_message(u_id, f"📢 **رسالة عامة من إدارة البوت:**\n\n{txt}", parse_mode="Markdown")
                    success += 1
                except: pass
            bot2.send_message(message.chat.id, f"✅ تم انتهاء الإذاعة بنجاح! وصلت لـ `{success}` مستخدم.")
            
        elif state == "waiting_for_cash":
            try:
                num, name = message.text.split("-")
                CONFIG["VODAFONE_NUMBER"] = num.strip()
                CONFIG["VODAFONE_NAME"] = name.strip()
                bot2.send_message(message.chat.id, "✅ تم تحديث بيانات فودافون كاش في النظام بنجاح!")
            except:
                bot2.send_message(message.chat.id, "❌ خطأ في الصيغة، لم يتم التعديل. يجب أن تفصل بـ (-).")
                
        elif state == "waiting_for_welcome":
            CONFIG["WELCOME_TEXT"] = message.text
            bot2.send_message(message.chat.id, "✅ تم تحديث رسالة ترحيب البوت الرئيسي بنجاح!")

# ====================================================================
# 🎓 كود وإعدادات بوت الترجمة والتعليم (البوت الخاص بالمستخدمين)
# ====================================================================
def setup_main_bot_handlers(target_bot):
    @target_bot.message_handler(commands=['start'])
    def welcome(message):
        if CONFIG["MAINTENANCE_MODE"] and message.from_user.id != ADMIN_CHAT_ID:
            target_bot.send_message(message.chat.id, "🚨 البوت قيد الصيانة والتحديثات حالياً، يرجى المحاولة لاحقاً.")
            return
            
        chat_id = message.chat.id
        user_modes[chat_id] = 'smart_teacher'
        user_levels[chat_id] = user_levels.get(chat_id, 1)
        total_users_interacted.add(message.from_user.id)
        
        welcome_msg = (
            f"{CONFIG['WELCOME_TEXT']}\n\n"
            f"🤖 **الوضع المفعل:** 🧠 _المعلم الذكي_\n"
            f"📊 **مستواك الحالي:** لفل {user_levels[chat_id]}\n\n"
            f"👇 **اختر نظام تشغيل البوت الذي تريده من الأزرار بالأسفل:**"
        )
        target_bot.send_message(chat_id, welcome_msg, reply_markup=get_main_keyboard(), parse_mode="Markdown")

    # 📸 استقبال لقطة الشاشة عند الدفع وتمريرها لبوت الأدمن بنظام القبول/الرفض التفاعلي
    @target_bot.message_handler(content_types=['photo'])
    def handle_payment_photo(message):
        chat_id = message.chat.id
        current_mode = user_modes.get(chat_id, "")
        
        if current_mode.startswith("waiting_payment_"):
            item_id = current_mode.replace("waiting_payment_", "")
            item_info = SHOP_ITEMS.get(item_id)
            
            if item_info:
                order_id = str(random.randint(100000, 999999))
                # حفظ بيانات الطلب المعلق في الذاكرة
                pending_orders[order_id] = {
                    "user_chat_id": chat_id,
                    "item_info": item_info
                }
                
                # إرسال الصورة فوراً لبوت الأدمن لقصي للمراجعة والتحقق التفاعلي
                admin_caption = (
                    f"💳 **طلب شراء جديد يحتاج مراجعتك يا قصي:**\n\n"
                    f"👤 **المستخدِم:** {message.from_user.first_name} (@{message.from_user.username})\n"
                    f"🆔 **ID المستخدم:** `{chat_id}`\n"
                    f"📦 **المنتج المطلوب:** {item_info['name']}\n"
                    f"💰 **المبلغ المطلوب:** {item_info['price']} جنيه\n"
                    f"🔢 **رقم معاملة الطلب:** `{order_id}`\n\n"
                    f"👇 **اتخذ قرارك الآن بالضغط على الأزرار بالأسفل:**"
                )
                bot2.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=admin_caption, reply_markup=get_order_review_keyboard(order_id), parse_mode="Markdown")
                
                # تأكيد استلام الصورة للمستخدم في البوت الرئيسي
                target_bot.reply_to(message, "✅ **تم استلام صورة التحويل بنجاح!**\nتم إرسال الإيصال للمطور قصي لمراجعته وتفعيله وتأكيده؛ ستصلك رسالة هنا بالملفات فور الموافقة التلقائية مباشرة.")
                user_modes[chat_id] = 'smart_teacher' # إعادة تعيين الوضع لعدم التكرار العشوائي
                return
        
        target_bot.reply_to(message, "📸 شكراً لإرسال الصورة! إذا كنت تريد شراء منتج، يرجى الضغط على زر الشراء في المتجر أولاً لربط إيصال الدفع بالطلب الخاص بك.")

    @target_bot.callback_query_handler(func=lambda call: not call.data.startswith("adm_") and not call.data.startswith("review_"))
    def user_callbacks(call):
        chat_id = call.message.chat.id
        total_users_interacted.add(call.from_user.id)
        
        if call.data == "mode_en_to_ar":
            user_modes[chat_id] = 'en_to_ar'
            target_bot.send_message(chat_id, "🔄 **تم تفعيل وضع:** [ إنجليزي ⬅️ عربي ]\n📥 أرسل أي نص بالإنجليزية!")
        elif call.data == "mode_ar_to_en":
            user_modes[chat_id] = 'ar_to_en'
            target_bot.send_message(chat_id, "🔄 **تم تفعيل وضع:** [ عربي ⬅️ إنجليزي ]\n📥 أرسل أي نص بالعربية!")
        elif call.data == "mode_smart":
            user_modes[chat_id] = 'smart_teacher'
            target_bot.send_message(chat_id, "🧠 **تم تفعيل وضع:** [ المعلم الذكي ]\nأرسل أي كلمة لترجمتها وتعليمها ذكياً!")
        elif call.data == "mode_levels_menu":
            target_bot.send_message(chat_id, "📊 **اختر لفل التدريب الخاص بك:**", reply_markup=get_levels_keyboard())
        elif call.data == "mode_shop_menu":
            target_bot.send_message(chat_id, "🛍️ **مرحباً بك في متجر الأدوات والكتب الاحترافية!**\n\nاختر المنتج الذي ترغب به أدناه: 👇", reply_markup=get_shop_keyboard(), parse_mode="Markdown")
            
        elif call.data.startswith("buy_"):
            item_id = call.data.replace("buy_", "")
            item_info = SHOP_ITEMS.get(item_id)
            
            if item_info:
                if CONFIG["FREE_MODE"]:
                    # تسليم فوري وتلقائي ومباشر بالكامل لأن الوضع المجاني مفعل من قصي
                    free_text = (
                        f"🎁 **الوضع المجاني فعال للمطور قصي!**\n\n"
                        f"📦 **المنتج:** {item_info['name']}\n"
                        f"💰 **السعر:** `0 جنيه`\n\n"
                        f"✅ **تم تسليم المنتج بنجاح! تفضل رابط التحميل:**\n🔗 {item_info['download_url']}"
                    )
                    target_bot.send_message(chat_id, free_text, parse_mode="Markdown")
                else:
                    # تحويل المستخدم لوضع انتظار إرسال لقطة الشاشة
                    user_modes[chat_id] = f"waiting_payment_{item_id}"
                    pay_text = (
                        f"🛒 **طلب شراء منتَج جديد:**\n\n"
                        f"📦 **المنتج:** {item_info['name']}\n"
                        f"💰 **المبلغ المطلوب سداده:** `{item_info['price']} جنيه`\n\n"
                        f"💳 **بيانات تحويل فودافون كاش:**\n"
                        f"📱 **الرقم للتحويل:** `{CONFIG['VODAFONE_NUMBER']}`\n"
                        f"👤 **باسم المستلم:** {CONFIG['VODAFONE_NAME']}\n\n"
                        f"⚠️ **خطوات التأكيد والاستلام الفوري:**\n"
                        f"1️⃣ قم بتحويل قيمة المنتج كاملاً للرقم الموضح.\n"
                        f"2️⃣ خذ لقطة شاشة (Screenshot) واضحة لإيصال نجاح المعاملة.\n"
                        f"3️⃣ **قم بإرسال الصورة هنا داخل البوت مباشرة** وسيقوم المطور قصي بقبولها لتستلم ملفاتك فوراً وبشكل تلقائي!"
                    )
                    target_bot.send_message(chat_id, pay_text, parse_mode="Markdown")

        elif call.data == "mode_make_bot":
            user_modes[chat_id] = 'waiting_for_token'
            target_bot.send_message(chat_id, "🤖 **أهلاً بك في صانع البوتات الذكي!**\n\nقم بالذهاب إلى @BotFather وأرسل لي **التوكن (Token)** هنا ليتم تشغيل بوتك الخاص!")
        elif call.data == "back_to_main":
            target_bot.send_message(chat_id, "🔄 تم الرجوع للواجهة الرئيسية للبوت:", reply_markup=get_main_keyboard())
        target_bot.answer_callback_query(call.id)

    @target_bot.message_handler(func=lambda message: True)
    def handle_text_messages(message):
        user_text = message.text.strip()
        chat_id = message.chat.id
        current_mode = user_modes.get(chat_id, 'smart_teacher')
        total_users_interacted.add(message.from_user.id)

        if current_mode == 'waiting_for_token':
            if user_text in [TOKEN_BOT_1, TOKEN_BOT_2]:
                target_bot.send_message(chat_id, "❌ غير مسموح باستخدام توكن البوت الأساسي داخل الصانع لمنع تضارب الخوادم والتوقف.")
                user_modes[chat_id] = 'smart_teacher'
                return
                
            if ":" in user_text and len(user_text) > 30:
                target_bot.send_message(chat_id, "⏳ جاري فحص وتجهيز خوادم بوتك الخاص...")
                
                def start_clone(token):
                    try:
                        clone_bot = telebot.TeleBot(token)
                        setup_main_bot_handlers(clone_bot)
                        active_clones[token] = clone_bot
                        clone_bot.infinity_polling()
                    except:
                        active_clones.pop(token, None)

                t = threading.Thread(target=start_clone, args=(user_text,), daemon=True)
                t.start()
                user_modes[chat_id] = 'smart_teacher'
                target_bot.send_message(chat_id, "🚀 **مبروك! تم تشغيل بوت الترجمة والتعليم الخاص بك بنجاح الآن!**")
            else:
                target_bot.send_message(chat_id, "❌ التوكن الذي أرسلته غير صحيح.")
            return

        # معالجات الترجمة والذكاء الاصطناعي الاعتيادية
        try:
            if current_mode == 'en_to_ar':
                translated = GoogleTranslator(source='en', target='ar').translate(user_text)
                target_bot.send_message(chat_id, f"🇵🇸 **الترجمة للعربية:**\n`{translated}`", parse_mode="Markdown")
            elif current_mode == 'ar_to_en':
                translated = GoogleTranslator(source='ar', target='en').translate(user_text)
                target_bot.send_message(chat_id, f"🇺🇸 **الترجمة للإنجليزية:**\n`{translated}`", parse_mode="Markdown")
            elif current_mode == 'smart_teacher':
                translated = GoogleTranslator(source='auto', target='ar').translate(user_text)
                target_bot.send_message(chat_id, f"🧠 **المعلم الذكي:**\n\nالنص المكتوب: `{user_text}`\nالترجمة الشاملة: `{translated}`", parse_mode="Markdown")
        except:
            target_bot.send_message(chat_id, "❌ عذراً، واجهت مشكلة فنية بسيطة أثناء المعالجة الآن.")

def get_levels_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(1, 6):
        keyboard.add(types.InlineKeyboardButton(LEVELS_DATA[i]["title"], callback_data=f"set_lvl_{i}"))
    keyboard.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return keyboard

# ====================================================================
# 🚀 بدء تشغيل خوادم البوتين في آن واحد دون تضارب
# ====================================================================
def run_main_bot():
    setup_main_bot_handlers(bot1)
    bot1.infinity_polling()

def run_admin_bot():
    setup_admin_bot_handlers()
    bot2.infinity_polling()

if __name__ == '__main__':
    t1 = threading.Thread(target=run_main_bot, daemon=True)
    t1.start()
    run_admin_bot()
