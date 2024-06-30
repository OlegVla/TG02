#Для того чтобы добавить возможность получения прогноза погоды для города
#Москва с использованием OpenWeatherMap API, вам нужно зарегистрироваться на сайте OpenWeatherMap
# и получить API ключ (токен). Затем вы можете использовать этот ключ для получения данных о погоде.

#Вот обновленный код вашего бота с добавлением функции для получения прогноза погоды:

import random
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN,WEATHER_API_KEY
from gtts import gTTS
import os


# Ваш API ключ OpenWeatherMap

WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

# Функция для получения погоды
async def get_weather(city: str):
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                return f"Температура: {temperature}°C\nОписание: {description}"
            else:
                return "Не удалось получить данные о погоде."

# Прописываем хендлер и варианты ответов:
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://img.freepik.com/free-photo/adorable-looking-kitten-with-box_23-2150886284.jpg?size=626&ext=jpg',
        'https://img.freepik.com/premium-photo/a-cute-furry-cats-indoors_862994-171023.jpg?size=626&ext=jpg',
        'https://img.freepik.com/premium-photo/cute-burmese-kitten-curled-up_1308-139607.jpg?size=626&ext=jpg'
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    response = (
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, '
        'которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, '
        'особенно интеллектуальных компьютерных программ'
    )
    await message.answer(response)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.full_name}')
@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    #await message.answer("Этот бот умеет выполнять команды:\\n/start\\n/help\\n/minitraining")
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('sound2.m4a')
    await bot.send_audio(message.chat.id, audio)
    #await message.answer("Этот бот умеет выполнять команды:\\n/start\\n/help\\n/minitraining")

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.mp3")
    audio = FSInputFile('training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove("training.mp3")
@dp.message(Command('help'))
async def help(message: Message):
    response = (
        "Этот бот умеет выполнять команды:\n"
        "/start\n"
        "/help\n"
        "/weather - получить прогноз погоды для города Москва"
    )
    await message.answer(response)


# Новый хендлер для получения погоды
@dp.message(Command('weather'))
async def weather(message: Message):
    weather_info = await get_weather('Москва')
    await message.answer(weather_info)

#@dp.message()
#async def start(message: Message):
    #await message.answer("Приветики, я бот!")

#@dp.message()
#async def start(message: Message):
    #await message.send_copy(chat_id=message.chat.id)

@dp.message()
async def start(message: Message):
		if message.text.lower() == 'test':
				await message.answer('Тестируем')



@dp.message(Command('audio'))
async def audio(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\\n/start\\n/help\\n/minitraining")


if __name__ == "__main__":
    asyncio.run(main())
