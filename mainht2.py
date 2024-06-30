
import random
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
from gtts import gTTS
import os
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


# Обработчик команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.reply(
         "Привет! Я бот, который может преобразовать текст в речь. Отправь мне текст,\
        и я переведу его на английский и озвучу его для тебя.\
         Если задашь команду /voice я выведу голосовое сообщение. Если введёшь фото я сохраню его."
    )
#Помощь
@dp.message(Command('help'))
async def help(message: Message):
    response = (
        "Этот бот умеет выполнять команды:\n"
        "/start\n"
        "/help\n"
        "/voice - выводить голосовое сообщение\n"
        "Переводить введенный текст с руского на английски и озвучить перевод \n"
        "Сохранять введенные фото\n"
    )
    await message.answer(response)

#Вывод голосового сообщения
@dp.message(Command('voice'))
async def voice(message: Message):
    audio = FSInputFile('sound2.m4a')
    await bot.send_audio(message.chat.id, audio)

#Сохранение введенного фото
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await message.answer("Я сохранил это фото")
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')
# Обработчик произвольного текста
@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text

    # Перевод текста на английский
    translated_text = translator.translate(text, dest='en').text

    # Отправка переведенного текста пользователю
    await message.reply(f"Переведенный текст: {translated_text}")

    # Преобразование текста в речь
    tts = gTTS(text=translated_text, lang='en')
    filename = "output.mp3"
    tts.save(filename)

    audio = FSInputFile(filename)
    await bot.send_audio(chat_id=message.chat.id, audio=audio)

    # Удаляем временный файл после отправки
    os.remove(filename)


# Главная функция для запуска бота
async def main():
    await dp.start_polling(bot)


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
