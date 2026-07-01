import os
import requests
import asyncio
from telegram import Bot

# التوكن الخاص بك مدمج هنا
BOT_TOKEN = '8759522486:AAHfUEiwijT8N2WdL9WbRCDk8gXor_Ka-IM'
# ضع معرف الشات الخاص بك هنا (يجب أن يكون رقم يبدأ بـ -100 إذا كانت قناة)
CHAT_ID = 'ضع_معرف_الشات_هنا' 
# ضع مفتاح API-Football هنا
API_KEY = 'ضع_مفتاح_API_الخاص_بك_هنا'

bot = Bot(token=BOT_TOKEN)

async def check_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-apisports-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers).json()
        matches = response.get('response', [])
        
        if not matches:
            return

        for match in matches:
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            
            message = f"⚽ مباراة مباشرة:\n{home_team} {home_goals} - {away_goals} {away_team}"
            await bot.send_message(chat_id=CHAT_ID, text=message)
            
    except Exception as e:
        print(f"حدث خطأ: {e}")

async def main():
    print("البوت بدأ بالعمل...")
    while True:
        await check_live_matches()
        await asyncio.sleep(300) # يفحص كل 5 دقائق

if __name__ == '__main__':
    asyncio.run(main())
