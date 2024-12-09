import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.admin import router as admin_router
from handlers.handlers import router

# Определяем путь к файлу .env и загружаем его содержимое
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):  # Если файл .env существует, загружаем переменные окружения
    load_dotenv(dotenv_path)

# Инициализация Dispatcher для обработки входящих обновлений
dp = Dispatcher()

# Инициализация объекта Bot с использованием API токена из переменных окружения
bot = Bot(os.environ['BOT_API'])


# Главная асинхронная функция, которая включает в себя роутеры и запускает бота
async def main() -> None:
    dp.include_router(admin_router)  # Подключаем роутер для админских команд
    dp.include_router(router)  # Подключаем основной роутер для обработки команд
    await dp.start_polling(bot)  # Запуск бота и начало опроса серверов Telegram


# Основная точка входа
if __name__ == "__main__":
    # Настройка логирования с выводом в файл log.txt, используя кодировку utf-8
    logging.basicConfig(level=logging.INFO,
                        # stream=sys.stdout)  # Можно настроить вывод в консоль
                        filename='log.txt', encoding='utf-8')  # Логи сохраняются в файл
    asyncio.run(main())  # Запускаем асинхронную функцию main
