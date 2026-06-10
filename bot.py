import sqlite3
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

ITEMS_PER_PAGE = 5  # عدد المودات التي تظهر في الصفحة الواحدة

# --- 1. إنشاء قاعدة البيانات وإضافة مودات تجريبية ---
def init_db():
    conn = sqlite3.connect('minecraft_mods.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            version_type TEXT, -- Java أو Bedrock
            category TEXT,     -- التصنيف (مثلاً: Utility, Weapons, Magic)
            description TEXT,
            download_url TEXT
        )
    ''')
    
    # إضافة عينات للتأكد من عمل نظام الصفحات
    cursor.execute("SELECT COUNT(*) FROM mods")
    if cursor.fetchone()[0] == 0:
        sample_mods = [
            ("X-Ray Ultimate", "Java", "Utility", "مود كشف الخامات تحت الأرض.", "https://example.com/xray"),
            ("VeinMiner", "Java", "Utility", "تعدين عرق الخامات كامل بضربة واحدة.", "https://example.com/veinminer"),
            ("OptiFine", "Java", "Utility", "تحسين أداء اللعبة وزيادة الـ FPS مع دعم الفريمات.", "https://example.com/optifine"),
            ("Sodium", "Java", "Utility", "بديل أوبcontain لزيادة الأداء بشكل خارق.", "https://example.com/sodium"),
            ("JourneyMap", "Java", "Utility", "خريطة تفاعلية لعالمك توضح الموبات والأماكن.", "https://example.com/journeymap"),
            ("Just Enough Items (JEI)", "Java", "Utility", "لعرض الوصفات وطرق صنع الأدوات.", "https://example.com/jei"),
            ("Furniture Addon", "Bedrock", "Decoration", "إضافة أثاث واقعي لنسخة الجوال والويندوز.", "https://example.com/furniture"),
        ]
        cursor.executemany("INSERT INTO mods (name, version_type, category, description, download_url) VALUES (?, ?, ?, ?, ?)", sample_mods)
        conn.commit()
    conn.close()

# --- 2. الأوامر والقوائم ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرئيسية: اختيار نوع اللعبة"""
    keyboard = [
        [
            InlineKeyboardButton("💻 مودات جافا (Java)", callback_data="type_Java"),
            InlineKeyboardButton("📱 مودات بيدروك (Bedrock)", callback_data="type_Bedrock")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🤖 أهلاً بك في بوت مودات ماين كرافت!\n\nاختر نوع النسخة التي تلعب بها لتصفح المودات:", reply_markup=reply_markup)

async def handle_menus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """المحرك الرئيسي للتحكم بالأزرار والتنقل"""
    query = update.callback_query
    await query.answer()
    data = query.data

    # 1. قائمة التصنيفات بناءً على النوع (Java / Bedrock)
    if data.startswith("type_"):
        selected_type = data.split("_")[1]
        
        conn = sqlite3.connect('minecraft_mods.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM mods WHERE version_type=?", (selected_type,))
        categories = cursor.fetchall()
        conn.close()

        keyboard = []
        for cat in categories:
            keyboard.append([InlineKeyboardButton(f"📂 {cat[0]}", callback_data=f"cat_{selected_type}_{cat[0]}_0")])
        
        keyboard.append([InlineKeyboardButton("🔙 العودة للرئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"👇 اختر تصنيف المودات لنسخة **{selected_type}**:", reply_markup=reply_markup, parse_mode="Markdown")

    # 2. عرض المودات داخل التصنيف مع نظام الصفحات (Pagination)
    elif data.startswith("cat_"):
        _, v_type, category, page_str = data.split("_")
        current_page = int(page_str)

        conn = sqlite3.connect('minecraft_mods.db')
        cursor = conn.cursor()
        
        # جلب العدد الإجمالي لحساب الصفحات
        cursor.execute("SELECT COUNT(*) FROM mods WHERE version_type=? AND category=?", (v_type, category))
        total_items = cursor.fetchone()[0]
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

        # جلب مودات الصفحة الحالية فقط باستخدام LIMIT و OFFSET
        offset = current_page * ITEMS_PER_PAGE
        cursor.execute("SELECT id, name FROM mods WHERE version_type=? AND category=? LIMIT ? OFFSET ?", 
                       (v_type, category, ITEMS_PER_PAGE, offset))
        mods = cursor.fetchall()
        conn.close()

        keyboard = []
        # أزرار المودات
        for mod_id, mod_name in mods:
            keyboard.append([InlineKeyboardButton(f"🔹 {mod_name}", callback_data=f"mod_{mod_id}")])
            
        # أزرار التنقل بين الصفحات (التالي والسابق)
        nav_buttons = []
        if current_page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"cat_{v_type}_{category}_{current_page - 1}"))
        if current_page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("التالي ➡️", callback_data=f"cat_{v_type}_{category}_{current_page + 1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)

        keyboard.append([InlineKeyboardButton("🔙 العودة للتصنيفات", callback_data=f"type_{v_type}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        page_text = f"📦 مودات {category} ({v_type}) - [صفحة {current_page + 1}/{max(1, total_pages)}]:\nاختر المود لعرض التفاصيل والتحميل:"
        await query.edit_message_text(page_text, reply_markup=reply_markup)

    # 3. عرض تفاصيل المود المختار ورابط التحميل
    elif data.startswith("mod_"):
        mod_id = data.split("_")[1]
        
        conn = sqlite3.connect('minecraft_mods.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, version_type, category, description, download_url FROM mods WHERE id=?", (mod_id,))
        mod = cursor.fetchone()
        conn.close()

        if mod:
            name, v_type, category, desc, url = mod
            text = f"⚙️ **اسم المود:** {name}\n" \
                   f"📌 **النسخة:** {v_type}\n" \
                   f"🗂️ **التصنيف:** {category}\n\n" \
                   f"📝 **الوصف:**\n{desc}"
            
            keyboard = [
                [InlineKeyboardButton("📥 تحميل المود", url=url)],
                [InlineKeyboardButton("🔙 العودة للقائمة", callback_data=f"cat_{v_type}_{category}_0")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    # 4. العودة للقائمة الرئيسية
    elif data == "main_menu":
        keyboard = [
            [
                InlineKeyboardButton("💻 مودات جافا (Java)", callback_data="type_Java"),
                InlineKeyboardButton("📱 مودات بيدروك (Bedrock)", callback_data="type_Bedrock")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🤖 اختر نوع النسخة التي تلعب بها لتصفح المودات:", reply_markup=reply_markup)

# --- 3. تشغيل البوت ---
if __name__ == '__main__':
    init_db()  # تهيئة قاعدة البيانات والتأكد من وجود الجداول البيانات
    
    # ⚠️ ضع هنا التوكن الخاص ببوتك من BotFather
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" 
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_menus))
    
    print("🤖 البوت يعمل الآن وتلقى الأوامر...")
    application.run_polling()
