from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from bot.database.database import init_database
from bot.handlers import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def start_bot():
    await init_database()
    print("База данных инициализирована")


async def main():
    dp.include_router(router=router)
    dp.startup.register(start_bot)
    await dp.start_polling(bot, skip_updates=True)