import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from bs4 import BeautifulSoup


API_TOKEN = "Сюда пишите свой токен"
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

#гет запрос на сайт с музыкой 
async def get_mp3_link(message):
    url = f"https://rus.hitmotop.com/search?q={message}&_pjax=%23pjax-container"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    first_link_element = soup.find('a', class_='track__download-btn')
    if first_link_element:
        first_link = first_link_element.get('href')
        return first_link
    else:
        return None
#Отправление сообщения с песней 
@dispatcher.message_handler()
async def process_message(message: Message):
    mp3_link = await get_mp3_link(message.text)
    if mp3_link:
        response = requests.get(mp3_link)
        if response.status_code == 200:
            audio_content = response.content
            await bot.send_audio(message.chat.id, audio_content, title=message.text)
    else:
        await message.answer("Sorry, I couldn't find the mp3 link.")

async def main():
    await dispatcher.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
