# -*- coding: utf-8 -*-
import os
import sys
import io
import requests
import asyncio
from telegram import Bot

# ضبط ترميز المخرجات لدعم اللغة العربية والرموز
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# قراءة الإعدادات من متغيرات البيئة في Railway
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
API_KEY = os.getenv('API_KEY')

bot = Bot(token=BOT_TOKEN)

async def check_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-apisports-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers).json()
        matches = response.get('response', [])
        
        if not matches:
            print("لا توجد مباريات مباشرة حالياً.")
            return

        for match in matches:
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            
            message = f"⚽ مباراة مباشرة:\n{home_team} {home_goals} - {away_goals} {away_team}"
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"تم إرسال تحديث: {home_team} vs {away_team}")
            
    except Exception as e:
        print(f"حدث خطأ أثناء جلب البيانات: {e}")

async def main():
    print("البوت بدأ بالعمل بنجاح...")
    while True:
        await check_live_matches()
        # الانتظار لمدة 5 دقائق (300 ثانية) قبل الفحص التالي
        await asyncio.sleep(300) 

if __name__ == '__main__':
    asyncio.run(main())
