import asyncio
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "8593187949:AAEIt1yRfAwNctcc4uSUh2VpizaovD9lQuc")  # Замените на реальный токен
SHEET_ID = "1Fsyx7fpelQAkAW_xjtI8taT-d_NmdOn-4_wYDdiQ6JY"  # ID вашей таблицы

# Google Sheets авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Подключаем таблицу
try:
    sheet = client.open_by_key(SHEET_ID).worksheet("Сводная_ежедневно")
except:
    # Если лист не существует — создаём
    spreadsheet = client.open_by_key(SHEET_ID)
    sheet = spreadsheet.add_worksheet(title="Сводная_ежедневно", rows=1000, cols=20)
    sheet.append_row(["Дата", "Прораб", "Вид_работ", "Код_работ", "Ед_изм", "План", "Факт", "Причина", "Статус", "Время", "Отправитель"])

# === КОМАНДЫ БОТА ===
@dp.message(CommandStart())
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Тест: записать в таблицу")],
            [KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "✅ Бот ГПР запущен!\n"
        "Выберите действие:",
        reply_markup=kb
    )

@dp.message(lambda msg: msg.text == "✅ Тест: записать в таблицу")
async def test_record(message: Message):
    try:
        sheet.append_row([
            datetime.now().strftime("%d.%m.%Y"),
            "Тестовый_прораб",
            "К2",
            "К2",
            "м.п.",
            "10",
            "8",
            "Тестовая причина",
            "⚠️ Невыполнено",
            datetime.now().strftime("%H:%M"),
            message.from_user.username or "unknown"
        ])
        await message.answer(f"✅ Запись добавлена в таблицу!\nДата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    except Exception as e:
        await message.answer(f"❌ Ошибка записи в таблицу:\n{str(e)}")

@dp.message(lambda msg: msg.text == "ℹ️ О боте")
async def about(message: Message):
    await message.answer(
        "🤖 Бот автоматизации ГПР «Новгородский_ЮГ»\n"
        "Версия: 1.0\n"
        "Статус: ✅ Работает\n\n"
        "Команды:\n"
        "/start — главное меню"
    )

# === ЗАПУСК БОТА ===
async def main():
    print("🚀 Бот запущен и готов к работе!")
    print(f"Дата запуска: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
