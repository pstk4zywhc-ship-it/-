import os
import zipfile
import json
import uuid
import telebot

# التوكن الخاص بك
BOT_TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(BOT_TOKEN)

def create_manifest(name="Converted Pack"):
    """إنشاء ملف manifest.json المتوافق مع نسخة البيدروك وتوليد الـ UUID تلقائياً"""
    manifest = {
        "format_version": 2,
        "header": {
            "description": "Converted from Java to Bedrock via Bot",
            "name": name,
            "uuid": str(uuid.uuid4()),
            "version": [1, 0, 0],
            "min_engine_version": [1, 16, 0]
        },
        "modules": [
            {
                "description": "Converted from Java to Bedrock via Bot",
                "type": "resources",
                "uuid": str(uuid.uuid4()),
                "version": [1, 0, 0]
            }
        ]
    }
    return json.dumps(manifest, indent=4)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي ملف حزمة الأنسجة بصيغة .zip وسأقوم بتحويلها فوراً إلى ملف .mcpack جاهز لماينكرافت الجوال والويندوز 10.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_name = message.document.file_name
    
    # التأكد من أن الملف بصيغة zip لضمان فك وقراءة الملفات بشكل سليم
    if not file_name.endswith('.zip'):
        bot.reply_to(message, "عذرًا، يرجى تحويل الحزمة إلى صيغة .zip أولاً ثم إرسالها لتتم معالجتها.")
        return

    bot.reply_to(message, "جاري تحويل الملف وصناعة الـ Manifest... انتظر لحظة.")
    
    # تحميل الملف من التلغرام
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    input_zip = f"downloaded_{message.chat.id}.zip"
    output_mcpack = file_name.replace('.zip', '.mcpack')
    
    with open(input_zip, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    try:
        pack_name = file_name.replace('.zip', '')
        manifest_data = create_manifest(pack_name)
        
        # فتح ملف الـ zip وإضافة الـ manifest.json في المسار الرئيسي للحزمة
        with zipfile.ZipFile(input_zip, 'a') as z:
            z.writestr('manifest.json', manifest_data)
            
        # تغيير الامتداد إلى mcpack
        os.rename(input_zip, output_mcpack)
        
        # إرسال الملف النهائي للمستخدم
        with open(output_mcpack, 'rb') as mcpack_file:
            bot.send_document(message.chat.id, mcpack_file, caption="تفضل! تم التحويل بنجاح، اضغط على الملف ليفتح في ماينكرافت مباشرة.")
            
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء المعالجة: {str(e)}")
    finally:
        # تنظيف الملفات المؤقتة من السيرفر للحفاظ على المساحة
        if os.path.exists(input_zip): os.remove(input_zip)
        if os.path.exists(output_mcpack): os.remove(output_mcpack)

# تشغيل البوت
bot.infinity_polling()
