# ====================================================================
# 🎛️ تحديث أزرار القائمة الرئيسية
# ====================================================================
def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("🇺🇸 ➡️ 🇵🇸 English to Arabic", callback_data="mode_en_to_ar"),
        types.InlineKeyboardButton("🇵🇸 ➡️ 🇺🇸 Arabic to English", callback_data="mode_ar_to_en"),
        types.InlineKeyboardButton("🧠 Smart Teacher | المعلم الذكي", callback_data="mode_smart"),
        types.InlineKeyboardButton("🗣️ كيف أنطقها؟ (تعريب النطق)", callback_data="mode_phonetic"), # الخيار الجديد
        types.InlineKeyboardButton("❓ هل تقدر؟ (تحدي الذكاء)", callback_data="mode_challenge"),
        types.InlineKeyboardButton("📊 تقييم المستوى وتحديد اللفل (1-5)", callback_data="mode_levels_menu"),
        types.InlineKeyboardButton("🛍️ متجر الأدوات الاحترافية (Shop)", callback_data="mode_shop_menu"),
        types.InlineKeyboardButton("🤖 اصنع بوت ترجمة خاص بك مجاناً", callback_data="mode_make_bot")
    )
    return keyboard

# ====================================================================
# 🎓 تعديل معالجات الأحداث (داخل setup_bot_handlers)
# ====================================================================
    # (داخل دالة user_callbacks)
    elif call.data == "mode_phonetic":
        GlobalConfig.user_modes[chat_id] = 'phonetic_helper'
        target_bot.send_message(chat_id, "🗣️ **تم تفعيل وضع: [ كيف أنطقها؟ ]**\n\nأرسل أي كلمة بالإنجليزية وسأكتب لك طريقة نطقها بالعربي فوراً!")

    # (داخل دالة handle_text_messages - ضع هذا الجزء في بداية الدالة قبل المعالجة العادية)
    if current_mode == 'phonetic_helper':
        # يمكنك إضافة أي كلمات هنا في هذا القاموس
        pronunciation_map = {
            "bag": "باغ", "hello": "هالو", "apple": "أبل", 
            "good": "غود", "school": "سكول", "thank you": "ثانك يو",
            "cat": "كات", "dog": "دوغ", "book": "بوك", "python": "بايثون"
        }
        word_lower = user_text.lower()
        pronunciation = pronunciation_map.get(word_lower, "عذراً، لم أضف هذه الكلمة في قاموسي بعد!")
        target_bot.send_message(chat_id, f"🗣️ النطق هو: **{pronunciation}**")
        return # الخروج من الدالة بعد إرسال النطق
