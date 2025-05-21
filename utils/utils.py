import os
import asyncio
import requests
from loguru import logger
from bs4 import BeautifulSoup
from random import choice
from aiogram import Bot
from dotenv import find_dotenv, load_dotenv
import re

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002531397827  # замените на свой ID

bot = Bot(token=TOKEN)

def escape_markdown(text):
    escape_chars = r'_*[]()~>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def send_random_joke():
    while True:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            response = requests.get('https://www.anekdot.ru/random/anekdot/ ', headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                jokes = soup.find_all('div', class_='text')
                if jokes:
                    anekdot = choice(jokes).get_text(strip=True)
                else:
                    anekdot = "Не найдено анекдотов на странице"
            else:
                anekdot = f"Ошибка получения страницы (статус {response.status_code})"
            
            escaped_joke = escape_markdown(anekdot)
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"🎭 *Анекдот дня:*\n\n{escaped_joke}",
                parse_mode="MarkdownV2"
            )
            logger.info(f"Опубликован анекдот: {anekdot}")
        
        except Exception as e:
            logger.error(f"Ошибка при отправке анекдота: {e}")
        
        await asyncio.sleep(86400)  # раз в сутки

if __name__ == "__main__":
    logger.add("bot.log", rotation="daily", level="INFO")
    asyncio.run(send_random_joke())