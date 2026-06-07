import telebot
from telebot import types
import cloudscraper
import time
import re

TOKEN = "8991347836:AAFjIPf0Nggic9kfto7VuCsHP3QvUiwhJ0M"
bot = telebot.TeleBot(TOKEN, num_threads=4)

ATERNOS_USER = "qusai2000"
ATERNOS_PASS = "qusai123@"
ADMIN_USERNAME = "sssss111126"

# قاموس اللغات المتكامل
LANGUAGES = {
    'ar': {
        'welcome': "🚀 أهلاً بك يا قُصي في لوحة تحكم أترنوس المتطورة!",
        'btn_servers': "📂
