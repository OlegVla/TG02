
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
import pyaudio
import wave


bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


# Обработчик команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.reply(
        "Привет! Я бот, который может преобразовать текст в речь. Отправь мне текст, и я переведу его на английский и озвучу его для тебя.")


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

def get_device_index(pyaudio_instance, is_input=True):
    device_count = pyaudio_instance.get_device_count()
    for i in range(device_count):
        device_info = pyaudio_instance.get_device_info_by_index(i)
        if is_input and device_info['maxInputChannels'] > 0:
            return i
        elif not is_input and device_info['maxOutputChannels'] > 0:
            return i
    return None



def record_audio(filename, record_seconds=5, channels=1, rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()

    input_device_index = get_device_index(audio, is_input=True)
    if input_device_index is None:
        raise Exception("No input device found")

    # Запись звука
    stream = audio.open(format=pyaudio.paInt16, channels=channels,rate=rate, input=True,frames_per_buffer=chunk, input_device_index=input_device_index)
    print("Recording...")

    frames = []

    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Завершение записи
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Сохранение в файл
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_audio(filename):
    wf = wave.open(filename, 'rb')
    audio = pyaudio.PyAudio()

    output_device_index = get_device_index(audio, is_input=False)
    if output_device_index is None:
        raise Exception("No output device found")

    # Открытие потока для воспроизведения
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

    data = wf.readframes(1024)

    # Воспроизведение звука
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Завершение воспроизведения
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    filename = "output.wav"
    record_audio(filename)
    play_audio(filename)

# Главная функция для запуска бота
async def main():
    await dp.start_polling(bot)


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
