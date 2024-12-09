import sys
import os
from dotenv import load_dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers.handlers import router
from handlers.handlers import router as admin_router

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
dp = Dispatcher()

bot = Bot(os.environ['BOT_API'])





async def main() -> None:
    dp.include_router(admin_router)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout)
                        # filename='log.txt', encoding='utf-8')
    asyncio.run(main())
