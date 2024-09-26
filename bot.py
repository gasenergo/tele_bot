import asyncio
from aiogram import Bot, Dispatcher, types, F
import logging
from dotenv import load_dotenv
import os
from data import data 

load_dotenv()  # Загружаем переменные из .env файла
API_TOKEN = os.getenv('API_TOKEN')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Создаем экземпляр бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(F.CommandStart())
async def send_welcome(message: types.Message):
    logging.info(f"Received /start command from {message.from_user.id}")
    await message.answer("Привет! Я ваш бот.")

# Обработчик текстовых сообщений
@dp.message(F.text)
async def handle_text_message(message: types.Message):
    logging.info(f"Received text message from {message.from_user.id}")
    text = message.text.title()
    results = list(filter(lambda entry: entry['Наименование'].startswith(text), data))
    # Форматируем ответ
    if len(results) > 1:
        response = "Есть несколько таких станций:\n" + "\n".join([f"Станция {entry['Наименование']}" for entry in results])+"\n".join([f"\nэто {results[0]['Дорога']} дорога"])
    elif len(results) == 1:
        response = "\n".join([f"Станция {entry['Наименование']}? Знаю, {entry['Дорога']} дорога" for entry in results])
    else:
        response = "Записи не найдены."
    await message.answer(response) 

# Основная асинхронная функция для запуска бота
async def main():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occurred: {e}")