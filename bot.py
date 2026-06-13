#!/usr/bin/env python3
import subprocess, sys, re, time, asyncio
from datetime import datetime
from collections import defaultdict

# تثبيت تلقائي
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# بيانات الحماية
failed = defaultdict(int)
blocked = {}
logs = defaultdict(list)

def check_password(pwd):
    score = 0
    notes = []
    if len(pwd) >= 12: score += 2
    else: notes.append("❌ الطول أقل من 12")
    if re.search(r'[A-Z]', pwd): score += 1
    else: notes.append("❌ لا يحتوي على حروف كبيرة")
    if re.search(r'[a-z]', pwd): score += 1
    else: notes.append("❌ لا يحتوي على حروف صغيرة")
    if re.search(r'\d', pwd): score += 1
    else: notes.append("❌ لا يحتوي على أرقام")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd): score += 2
    else: notes.append("❌ لا يحتوي على رموز خاصة")
    if score >= 6: res = "✅ قوية"
    elif score >= 4: res = "⚠️ متوسطة"
    else: res = "🔴 ضعيفة"
    return res, score, notes

def detect_phishing(text):
    keywords = ["تحديث حسابك", "تسجيل الدخول", "تأكيد", "تحقق", "كلمة المرور", "أمن"]
    for kw in keywords:
        if kw in text.lower():
            return f"⚠️ تحذير: كلمة '{kw}' مشبوهة"
    if re.search(r'https?://\S+', text):
        return "⚠️ تحذير: رابط خارجي غير موثوق"
    return None

async def start(update, context):
    await update.message.reply_text("🛡️ بوت أمني\nأرسل نص أو كلمة مرور للتحليل\n/log سجل\n/reset مسح")

async def log_cmd(update, context):
    uid = update.effective_user.id
    if not logs[uid]:
        await update.message.reply_text("لا يوجد سجل")
        return
    await update.message.reply_text("\n".join(logs[uid][-10:]))

async def reset_cmd(update, context):
    logs[update.effective_user.id] = []
    await update.message.reply_text("تم المسح")

async def handle(update, context):
    uid = update.effective_user.id
    if uid in blocked and time.time() < blocked[uid]:
        await update.message.reply_text("⛔ محظور مؤقتاً")
        return
    elif uid in blocked:
        del blocked[uid]
    
    text = update.message.text
    now = datetime.now().strftime("%H:%M:%S")
    
    # فحص التصيد
    phish = detect_phishing(text)
    if phish:
        await update.message.reply_text(phish)
        failed[uid] += 1
        logs[uid].append(f"[{now}] تصيد")
        if failed[uid] >= 3:
            blocked[uid] = time.time() + 300
            await update.message.reply_text("🚫 حظر 5 دقائق")
        return
    
    # تحليل كلمة المرور
    res, score, notes = check_password(text)
    notes_str = "\n".join(notes) if notes else "جميع المعايير جيدة"
    await update.message.reply_text(f"{res} ({score}/7)\n{notes_str}")
    logs[uid].append(f"[{now}] {res}")
    failed[uid] = 0

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("log", log_cmd))
    app.add_handler(CommandHandler("reset", reset_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ البوت شغال - توكل على الله")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
