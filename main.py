import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

API_TOKEN = "8257105888:AAEcJf7a5siSGXz5wfW6IE-fBcUJX-49U2Y"

# Ініціалізація бота з HTML
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ти написав: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
