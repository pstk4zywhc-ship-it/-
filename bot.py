async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال رسالة المستخدم والرد عليها عبر مزود مجاني تماماً"""
    user_message = update.message.text
    
    # إظهار أن البوت يكتب الآن
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # تحديد نموذج ومزود خدمة مجاني لا يتطلب API Key
        response = g4f.ChatCompletion.create(
            model=g4f.models.default, # استخدام النموذج الافتراضي المستقر
            provider=g4f.Provider.Blackbox, # مزود خدمة مجاني وسريع جداً وممتاز للعربية
            messages=[{"role": "user", "content": user_message}],
        )
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في الاتصال بالذكاء الاصطناعي. جرب إرسال الرسالة مرة أخرى.")
