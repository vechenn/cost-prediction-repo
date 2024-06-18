import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = '7356627228:AAEk6G-hk5DYNxS5aPVhSQl6BnqAp4Aq-n4'
FASTAPI_URL = 'http://127.0.0.1:8000/predict'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправьте мне CSV-файл для предсказания.')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.document.get_file()
    file_contents = await file.download_as_bytearray()

    # Отправка файла в FastAPI-приложение и получение предсказания
    try:
        response = requests.post(
            FASTAPI_URL,
            files={'file': ('data.csv', file_contents, 'text/csv')}
        )
        response.raise_for_status()
        prediction = response.json()
        
        await update.message.reply_text(
            f"Предсказания:\n"
            f"Неделя 1: {prediction['week_1']}\n"
            f"Неделя 2: {prediction['week_2']}\n"
            f"Неделя 3: {prediction['week_3']}\n"
            f"Неделя 4: {prediction['week_4']}"
        )
    except requests.RequestException as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

def main() -> None:
    # Создание Application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.MimeType("text/csv"), handle_file))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()