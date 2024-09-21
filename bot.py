import asyncio
from aiogram import Bot, Dispatcher, types, F
import logging
from config import API_TOKEN 

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
    await message.answer(message.text)

# Основная асинхронная функция для запуска бота
async def main():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occurred: {e}")