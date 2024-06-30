#Для создания Telegram-бота на Python с использованием библиотеки `alogram` для
# сохранения аудио файлов, отправленных пользователем, вам понадобятся следующие шаги:

#1. Установите необходимые библиотеки:



# Напишите код для вашего бота. Ниже приведен пример кода, который сохраняет
# аудио файлы в папку `audio`.

from config import TOKEN
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType


# Установите токен бота, который вы получили от BotFather


# Создайте папку для хранения аудио файлов, если она не существует
AUDIO_FOLDER = 'audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Создайте экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

# Установите уровень логирования
logging.basicConfig(level=logging.INFO)

@dp.message(lambda message: message.content_type == ContentType.VOICE)
async def handle_voice_message(message: types.Message):
    await message.reply("You sent a voice message!")



@dp.message(content_types=[types.ContentType.VOICE])
async def handle_voice_message(message: types.Message):
    voice = message.voice
    file_info = await bot.get_file(voice.file_id)
    file_path = file_info.file_path

    # Загрузите файл
    file_data = await bot.download_file(file_path)

    # Создайте путь для сохранения файла
    file_name = f'{voice.file_id}.ogg'
    file_full_path = os.path.join(AUDIO_FOLDER, file_name)

    # Сохраните файл
    with open(file_full_path, 'wb') as audio_file:
        audio_file.write(file_data)

    # Отправьте подтверждение пользователю
    await message.reply(f'Ваш аудио файл был сохранен как {file_name}')
if __name__ == '__main__':
    dp.start_polling(bot)



#1. **Импорт необходимых библиотек**: Импортируйте необходимые модули и функции.

#2. **Настройка**: Установите токен вашего бота и создайте папку `audio` для хранения аудио файлов.

#3. **Создание бота и диспетчера**: Создайте экземпляры бота и диспетчера.

#4. **Обработчик сообщений с аудио**: Определите обработчик для сообщений, содержащих
# голосовые сообщения (`types.ContentType.VOICE`). Обработчик загружает файл, сохраняет его
# в папку `audio` и отправляет подтвержден