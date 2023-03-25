import os
import subprocess
import telebot
import json
import sys
import vosk

# Устанавливаем ключ и создаем объект бота
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

# Создаем распознаватель
model = vosk.Model('vosk-model-small-ru-0.15')

# Обработчик сообщений, содержащих голосовые сообщения
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Сохраняем голосовое сообщение на диск
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)

    with open('voice.ogg', 'wb') as f:
        f.write(file)

    # Конвертируем голосовое сообщение в WAV формат
    subprocess.run(['ffmpeg', '-i', 'voice.ogg', '-ar', '16000', '-ac', '1', '-f', 'wav', 'voice.wav'])

    # Открываем файл с голосовым сообщением и распознаем его
    with open('voice.wav', 'rb') as f:
        data = f.read()

    recognizer = vosk.KaldiRecognizer(model, 16000)
    recognizer.AcceptWaveform(data)

    # Получаем результат распознавания голоса
    result = json.loads(recognizer.Result())

    # Возвращаем полученный текст сообщения боту в Telegram
    bot.send_message(message.chat.id, result['text'])

if __name__ == '__main__':
    # Запускаем бота
    bot.polling(none_stop=True)
