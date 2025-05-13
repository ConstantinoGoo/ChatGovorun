import sys
import os

# Добавляем корневую директорию проекта в sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
# Убедимся, что yandexgpt-python-main находится в project_root, а не на уровень выше
# Если yandexgpt-python-main это пакет ВНУТРИ ChatGovorun, то project_root это правильный путь.
# Если ChatGovorun сам является частью yandexgpt-python-main, то логика другая.
# Судя по list_dir, yandexgpt-python-main находится ВНУТРИ ChatGovorun.
sys.path.insert(0, project_root)

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yagpt
import os
import asyncio
from dotenv import load_dotenv
from yagpt import YandexGPTClient

# Инициализация логгера
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Загрузка переменных окружения
load_dotenv()

# Инициализация YandexGPT клиента
yagpt_api_key = os.getenv('YANDEXGPT_API_KEY')
yandex_catalog_id = os.getenv('YANDEX_CATALOG_ID') # Добавлено получение ID каталога

if not yagpt_api_key:
    logging.error("YANDEXGPT_API_KEY не найден в .env файле. Пожалуйста, добавьте его.")
    # exit()
if not yandex_catalog_id:
    logging.error("YANDEX_CATALOG_ID не найден в .env файле. Пожалуйста, добавьте его.")
    # exit()

# Проверяем, что оба значения есть, прежде чем инициализировать клиент
if yagpt_api_key and yandex_catalog_id:
    yagpt_client = YandexGPTClient(api_key=yagpt_api_key, catalog_id=yandex_catalog_id)
else:
    logging.error("Не удалось инициализировать YandexGPTClient из-за отсутствия API ключа или ID каталога.")
    # Можно установить yagpt_client в None или заглушку, чтобы избежать ошибок далее
    yagpt_client = None

# Инициализация бота
async def start(update: Update, context):
    await update.message.reply_text('Привет! Я бот, который свяжет тебя с Алисой.')

# Обработка сообщений
async def handle_message(update: Update, context):
    if not yagpt_client:
        await update.message.reply_text("Клиент YandexGPT не инициализирован. Проверьте настройки.")
        return
    message = update.message.text
    response = await yagpt_client.get_response(message)
    await update.message.reply_text(response)

def main():
    # Ваш токен Telegram бота
    token = 'YOUR_TELEGRAM_BOT_TOKEN'
    
    # Создание приложения
    application = Application.builder().token(token).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    application.run_polling(poll_interval=1.0)

async def test_yagpt_connection():
    """Функция для тестирования прямого запроса к YandexGPT."""
    if not yagpt_client:
        print("Клиент YandexGPT не инициализирован. Тестирование невозможно.")
        return
    
    # Проверка yagpt_api_key и yandex_catalog_id уже была выше при инициализации
    # но для теста можно оставить явную проверку ключа, если он нужен где-то еще отдельно
    if not yagpt_api_key or not yandex_catalog_id:
        print("YANDEXGPT_API_KEY или YANDEX_CATALOG_ID не настроен. Тестирование невозможно.")
        return

    test_message = "Привет, Яндекс GPT! Как дела?"
    print(f"Отправка тестового сообщения в YandexGPT: '{test_message}'")
    try:
        response = await yagpt_client.get_response(test_message)
        print(f"Ответ от YandexGPT: {response}")
    except Exception as e:
        print(f"Ошибка при тестировании YandexGPT: {e}")

if __name__ == '__main__':
    # Для тестирования соединения с YandexGPT, раскомментируйте следующую строку
    # и закомментируйте main():
    # main()
    asyncio.run(test_yagpt_connection())