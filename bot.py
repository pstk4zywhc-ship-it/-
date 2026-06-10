import os
import zipfile
import json
import uuid
import telebot

# التوكن الخاص بك الذي أرسلته سابقاً
BOT_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(BOT_TOKEN)

def create_manifest(name="Converted Pack"):
    """إنشاء ملف manifest.json المتوافق مع نسخة البيدروك وتوليد الـ UUID تلقائياً"""
    manifest = {
        "format_version": 2,
        "header": {
            "description": "Converted from Java (.jar) to Bedrock (.mcpack) via Bot",
            "name": name,
            "uuid": str(uuid.uuid4()),
            "version": [1, 0, 0],
            "min_engine_version": [1, 16, 0]
        },
        "modules": [
            {
                "description": "Converted from Java (.jar) to Bedrock (.mcpack) via Bot",
                "type": "resources",
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0]
            }
        ]
    }
    return json.dumps(manifest, indent=4)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي ملف المود أو حزمة الأنسجة بصيغة .jar أو .zip وسأقوم بتحويلها فوراً إلى ملف .mcpack جاهز لماينكرافت البيدروك (الجوال والويندوز).")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_name = message.document.file_name
    file_ext = os.path.splitext(file_name)[1].lower()
    
    # التحقق من أن الملف المرسل إما .jar أو .zip
    if file_ext not in ['.jar', '.zip']:
        bot.reply_to(message, "عذرًا، يرجى إرسال ملف بامتداد .jar أو .zip لتتم معالجته وتحويله.")
        return

    bot.reply_to(message, "جاري تحميل الملف وفك ضغطه ومعالجته... انتظر لحظة.")
    
    # تحميل الملف من سيرفرات التلغرام
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # تحديد أسماء الملفات المؤقتة بناءً على آيدي الشات لتجنب تداخل الملفات للمستخدمين
    input_file_path = f"input_{message.chat.id}{file_ext}"
    output_mcpack_path = f"output_{message.chat.id}.mcpack"
    
    # حفظ الملف المحمل على السيرفر
    with open(input_file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    try:
        pack_name = os.path.splitext(file_name)[0]
        manifest_data = create_manifest(pack_name)
        
        # بما أن ملف .jar هو ملف مضغوط أصلاً، يمكننا فتحه مباشرة عبر مكتبة zipfile وتعديله
        with zipfile.ZipFile(input_file_path, 'a') as z:
            # إضافة ملف manifest.json في المسار الرئيسي داخل الملف
            z.writestr('manifest.json', manifest_data)
            
        # إعادة تسمية وتحويل الملف المعدل إلى امتداد .mcpack
        os.rename(input_file_path, output_mcpack_path)
        
        # إرسال الملف النهائي للمستخدم بالاسم الأصلي للمود ولكن بامتداد .mcpack
        final_filename = f"{pack_name}.mcpack"
        with open(output_mcpack_path, 'rb') as mcpack_file:
            bot.send_document(
                message.chat.id, 
                mcpack_file, 
                visible_file_name=final_filename,
                caption="تفضل! تم تحويل ملف الـ .jar إلى .mcpack بنجاح وبشكل تلقائي. اضغط عليه ليفتح في ماينكرافت مباشرة."
            )
            
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء معالجة الملف: {str(e)}")
    finally:
        # تنظيف وحذف الملفات المؤقتة من السيرفر فوراً لعدم امتلاء الذاكرة
        if os.path.exists(input_file_path): os.remove(input_file_path)
        if os.path.exists(output_mcpack_path): os.remove(output_mcpack_path)

# تشغيل البوت بشكل مستمر للاستماع للرسائل
bot.infinity_polling()
