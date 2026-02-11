import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Ошибка: Не найден токен бота!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("✅ Бот ГПР запущен!\nГотов принимать отчёты.")

async def main():
    print("🚀 Бот запущен! Напишите /start в Telegram")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
