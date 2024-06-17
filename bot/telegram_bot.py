import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pandas as pd
import io

TELEGRAM_TOKEN = '7356627228:AAEk6G-hk5DYNxS5aPVhSQl6BnqAp4Aq-n4'
FASTAPI_URL = 'http://127.0.0.1:8000/predict'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте мне CSV-файл для предсказания.')

def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file_contents = file.download_as_bytearray()

    # Отправка файла в FastAPI-приложение и получение предсказания
    try:
        response = requests.post(
            FASTAPI_URL,
            files={'file': ('data.csv', file_contents, 'text/csv')}
        )
        response.raise_for_status()
        prediction = response.json()
        
        update.message.reply_text(
            f"Предсказания:n"
            f"Неделя 1: {prediction['week_1']}n"
            f"Неделя 2: {prediction['week_2']}n"
            f"Неделя 3: {prediction['week_3']}n"
            f"Неделя 4: {prediction['week_4']}"
        )
    except requests.RequestException as e:
        update.message.reply_text(f"Произошла ошибка: {e}")

def main() -> None:
    # Создание Updater и Dispatcher
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("text/csv"), handle_file))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()