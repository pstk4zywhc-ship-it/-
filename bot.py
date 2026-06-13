#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

# ------------------- التثبيت التلقائي للمكتبات -------------------
def install_packages():
    try:
        import telegram
    except ImportError:
        print("📦 جاري تثبيت المكتبات المطلوبة...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
        print("✅ تم التثبيت بنجاح")

install_packages()

# ------------------- المكتبات -------------------
import re
import time
from datetime import datetime
from collections import defaultdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ------------------- توكن البوت -------------------
TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"

# ------------------- قوائم الحماية -------------------
failed_attempts = defaultdict(int)
blocked_users = {}
user_log = defaultdict(list)

# ------------------- الحماية من التكرار -------------------
def is_blocked(user_id):
    if user_id in blocked_users and time.time() < blocked_users[user_id]:
        return True
    elif user_id in blocked_users:
        del blocked_users[user_id]
    return False

# ------------------- تحليل كلمة المرور -------------------
def password_strength(pwd):
    score, notes = 0, []
    if len(pwd) >= 12:
        score += 2
    else:
        notes.append("❌ الطول أقل من 12")
    if re.search(r'[A-Z]', pwd):
        score += 1
    else:
        notes.append("❌ لا يحتوي على حروف كبيرة")
    if re.search(r'[a-z]', pwd):
        score += 1
    else:
        notes.append("❌ لا يحتوي على حروف صغيرة")
    if re.search(r'\d', pwd):
        score += 1
    else:
        notes.append("❌ لا يحتوي على أرقام")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd):
        score += 2
    else:
        notes.append("❌ لا يحتوي على رموز خاصة")
    if score >= 6:
        result = "✅ قوية جداً"
    elif score >= 4:
        result = "⚠️ متوسطة"
    else:
        result = "🔴 ضعيفة"
    return result, score, notes

# ------------------- كشف التصيد -------------------
def detect_phishing(text):
    phishing_keywords = ["تحديث حسابك", "تسجيل الدخول", "أمن", "تأكيد", "بنجاح", "ربط", "تحقق", "كلمة المرور"]
    suspicious_links = re.findall(r'https?://[^\s]+', text)
    threat = []
    for kw in phishing_keywords:
        if kw in text.lower():
            threat.append(f"⚠️ كلمة مفتاحية خطيرة: {kw}")
    if suspicious_links:
        threat.append(f"🔗 روابط مشبوهة: {', '.join(suspicious_links)}")
    if "bit.ly" in text or "tinyurl" in text:
        threat.append("⚠️ رابط مختصر خطر")
    return threat if threat else None

# ------------------- الأوامر -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔐 تحليل كلمة مرور", callback_data="check_pwd")]]
    await update.message.reply_text(
        "🛡️ بوت الأمن السيبراني التعليمي\n\n"
        "✨ الأوامر المتاحة:\n"
        "• أرسل أي نص - لكشف التصيد\n"
        "• أرسل كلمة مرور - لتحليل قوتها\n"
        "• /log - عرض نشاطاتك\n"
        "• /reset - حذف سجلك\n"
        "• /start - إعادة تشغيل البوت\n\n"
        "🔒 هذا البوت لأغراض تعليمية فقط",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_log or not user_log[uid]:
        await update.message.reply_text("📭 لا يوجد سجل لك بعد.")
        return
    logs = user_log[uid][-10:]
    msg = "\n".join([f"• {l}" for l in logs])
    await update.message.reply_text(f"📋 آخر 10 أنشطة لك:\n\n{msg}")

async def reset_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_log[update.effective_user.id] = []
    await update.message.reply_text("✅ تم حذف سجلك بالكامل.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 المساعدة:\n\n"
        "1️⃣ لتحليل كلمة مرور:\n"
        "   فقط أرسلها في رسالة منفردة\n\n"
        "2️⃣ لكشف التصيد:\n"
        "   أرسل أي نص أو رابط مشبوه\n\n"
        "3️⃣ لإدارة سجلك:\n"
        "   /log - عرض السجل\n"
        "   /reset - مسح السجل\n\n"
        "⚠️ تذكر: لا ترسل كلمات مرور حقيقية!"
    )

# ------------------- معالجة الرسائل -------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    now = datetime.now().strftime("%H:%M:%S")
    
    # التحقق من الحظر
    if is_blocked(uid):
        await update.message.reply_text("⛔ ممنوع: تجاوزت الحد المسموح. حاول بعد 5 دقائق.")
        return
    
    # كشف التصيد أولاً
    phish = detect_phishing(text)
    if phish:
        warning = "\n".join(phish)
        await update.message.reply_text(f"⚠️ تحذير أمني: محاولة تصيد محتملة!\n\n{warning}")
        failed_attempts[uid] += 1
        user_log[uid].append(f"[{now}] 🚨 تصيد مكتشف")
        if failed_attempts[uid] >= 3:
            blocked_users[uid] = time.time() + 300
            await update.message.reply_text("🚫 تم حظرك 5 دقائق لكثرة المحاولات الخطيرة")
        return
    
    # تحليل كلمة المرور
    res, score, notes = password_strength(text)
    notes_text = "\n".join(notes) if notes else "✅ جميع المعايير مستوفاة"
    await update.message.reply_text(
        f"{res}\n"
        f"📊 النتيجة: {score}/7\n\n"
        f"📝 التفاصيل:\n{notes_text}"
    )
    user_log[uid].append(f"[{now}] 🔐 تحليل كلمة مرور - {res}")
    failed_attempts[uid] = 0

# ------------------- معالجة الأزرار -------------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🔐 أرسل كلمة المرور الآن (لن تُحفظ في أي مكان)")

# ------------------- التشغيل الرئيسي -------------------
def main():
    print("=" * 50)
    print("🔥 تشغيل بوت الأمن السيبراني...")
    print(f"📌 التوكن: {TOKEN[:10]}...")
    print("✅ البوت جاهز للعمل")
    print("=" * 50)
    
    app = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("log", log_command))
    app.add_handler(CommandHandler("reset", reset_log))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # تشغيل البوت
    print("🚀 بدء الاستماع للرسائل...")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
        print("🔄 تأكد من اتصال الإنترنت وتوكن البوت الصحيح")
        input("اضغط Enter للإغلاق...")
