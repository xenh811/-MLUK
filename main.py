import asyncio
from aiohttp import web
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# ТОКЕН БОТА
# TOKEN = "8257105888:AAFoBy0W2IjPK_6sWKf-DIQny1j87EFEggw" # локальний варіант

TOKEN = os.getenv("BOT_TOKEN") # токен вписується в рендері (environment variable Render)
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
async def handle(request):
    return web.Response(text="Bot is running")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    print("BOT STARTED ON RENDER (WEB MODE)")

    await start_web()             # 🔴 БЕЗ await НЕ ПРАЦЮЄ
    await dp.start_polling(bot)


#  КНОПКИ
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔔 Розклад дзвінків")],
        [KeyboardButton(text="📰 Наші соціальні мережі")],
        [KeyboardButton(text="📁 Корисні матеріали")],
        [KeyboardButton(text="👨‍🏫 Кабінет вчителя")],
        [KeyboardButton(text="📅 Мій розклад")]
    ],
    resize_keyboard=True
)

teacher_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Мій розклад")],
        [KeyboardButton(text="✏️ Редагувати розклад")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

# ================== ДАНІ ==================
BELLS = """🔔 Розклад дзвінків
0️⃣ 07:40 – 08:25
1️⃣ 08:30 – 09:15
2️⃣ 09:25 – 10:10
3️⃣ 10:20 – 11:05
4️⃣ 11:25 – 12:10
5️⃣ 12:30 – 13:15
6️⃣ 13:25 – 14:10
7️⃣ 14:20 – 15:05
"""

GOOGLE_DRIVE_LINK = "https://drive.google.com/ТУТ_ПОСИЛАННЯ"

SOCIALS_TEXT = (
    "📰 <b>Наші соціальні мережі:</b>\n\n"
    "📘 Facebook: https://www.facebook.com/profile.php?id=100063582906575\n"
    "🌐 Сайт: https://sites.google.com/view/mluk/%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BD%D0%B0-%D1%81%D1%82%D0%BE%D1%80%D1%96%D0%BD%D0%BA%D0%B0?authuser=0"
    "📣 Telegram: https://web.telegram.org/a/#-1001541377749"
)

teachers = {
    392199561: {
        "name": "Малик Олег Володимирович",
        "subject": "Інформатика",
        "schedule": {
            "Понеділок": "8-А, 8-Б",
            "Вівторок": "9-А",
            "Середа": "11-Г",
            "Четвер": "10-А",
            "Пʼятниця": "8-А"
        }
    }
}

# ================== START ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Вітаю 👋\nОбери пункт меню:",
        reply_markup=menu
    )

# ================== ОСНОВНЕ МЕНЮ ==================
@dp.message(lambda m: m.text == "🔔 Розклад дзвінків")
async def bells(message: types.Message):
    await message.answer(BELLS)

@dp.message(lambda m: m.text == "📁 Корисні матеріали")
async def materials(message: types.Message):
    await message.answer(f"📁 Корисні матеріали:\n{GOOGLE_DRIVE_LINK}")

@dp.message(lambda m: m.text == "📰 Наші соціальні мережі")
async def socials(message: types.Message):
    await message.answer(SOCIALS_TEXT, parse_mode="HTML")

# ================== КАБІНЕТ ВЧИТЕЛЯ ==================
@dp.message(lambda m: m.text == "👨‍🏫 Кабінет вчителя")
async def teacher_cabinet(message: types.Message):
    teacher = teachers.get(message.from_user.id)

    if not teacher:
        await message.answer("❌ Доступ заборонений.\nВаш Telegram ID не знайдено.")
        return

    await message.answer(
        f"👨‍🏫 <b>{teacher['name']}</b>\n"
        f"📘 Предмет: {teacher['subject']}\n\n"
        "Оберіть дію:",
        reply_markup=teacher_menu,
        parse_mode="HTML"
    )

@dp.message(lambda m: m.text == "📅 Мій розклад")
async def my_schedule(message: types.Message):
    teacher = teachers.get(message.from_user.id)
    if not teacher:
        return

    text = "<b>📅 Ваш розклад:</b>\n\n"
    for day, value in teacher["schedule"].items():
        text += f"<b>{day}:</b> {value}\n"

    await message.answer(text, parse_mode="HTML")

@dp.message(lambda m: m.text == "✏️ Редагувати розклад")
async def edit_info(message: types.Message):
    if message.from_user.id not in teachers:
        return

    await message.answer(
        "✏️ Введіть у форматі:\n<b>День: Класи</b>\n\n"
        "Приклад:\nПонеділок: 9-А, 10-Б",
        parse_mode="HTML"
    )

@dp.message(lambda m: ":" in m.text and m.from_user.id in teachers)
async def edit_schedule(message: types.Message):
    teacher = teachers[message.from_user.id]

    try:
        day, value = message.text.split(":", 1)
        day = day.strip()

        if day not in teacher["schedule"]:
            await message.answer("❌ Невірний день.")
            return

        teacher["schedule"][day] = value.strip()
        await message.answer(f"✅ Оновлено: <b>{day}</b>", parse_mode="HTML")

    except:
        await message.answer("❌ Помилка формату.")

@dp.message(lambda m: m.text == "⬅️ Назад")
async def back(message: types.Message):
    await message.answer("Головне меню:", reply_markup=menu)


async def main():
    print("Бот працює на Render ✔️")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

#  ЛОКАЛЬНИЙ ЗАПУСК (POLLING)
# async def main_local():
#     print("Бот запущено локально ✔️")
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main_local())



