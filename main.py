import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# -----------------------------
# ENV змінні (Render / локально)
# -----------------------------
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("BOT_TOKEN is not set in environment variables!")

WEBHOOK_PATH = "/webhook"

# Render встановлює RENDER_EXTERNAL_URL автоматично
BASE_URL = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8080")

WEBHOOK_URL = BASE_URL + WEBHOOK_PATH

# -----------------------------
# Ініціалізація бота
# -----------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer("Webhook працює! ✔️")


# -----------------------------
# Webhook запуск / зупинка
# -----------------------------
async def on_startup(app: web.Application):
    print("Setting webhook:", WEBHOOK_URL)
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app: web.Application):
    print("Deleting webhook...")
    await bot.delete_webhook()


# -----------------------------
# Aiohttp сервер
# -----------------------------
def main():
    app = web.Application()

    # підключаємо хендлери aiogram
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))   # Render передає PORT автоматично
    )

if __name__ == "__main__":
    main()
