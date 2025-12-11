import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



# ТОКЕН БОТА
# TOKEN = "8257105888:AAFoBy0W2IjPK_6sWKf-DIQny1j87EFEggw" локальний варіант

TOKEN = os.getenv("BOT_TOKEN") # токен вписується в рендері (environment variable Render)
bot = Bot(token=TOKEN)
dp = Dispatcher()



#  КНОПКИ
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔔 Розклад дзвінків")],
        [KeyboardButton(text="📰 Новини ліцею")],
        [KeyboardButton(text="📁 Корисні матеріали")],
        [KeyboardButton(text="👨‍🏫 Кабінет вчителя")],
        [KeyboardButton(text="📅 Мій розклад")]
    ],
    resize_keyboard=True
)


#  ДАНІ
BELLS = """
🔔 Розклад дзвінків

1️⃣ 08:30 – 09:15
2️⃣ 09:25 – 10:10
3️⃣ 10:20 – 11:05
4️⃣ 11:25 – 12:10
5️⃣ 12:20 – 13:05
6️⃣ 13:15 – 14:00
"""

GOOGLE_DRIVE_LINK = "ПОСИЛАННЯ_НА_GOOGLE_DRIVE"

NEWS = [
    "📢 10.09 — День здоров'я",
    "📢 15.09 — Батьківські збори"
]

teachers = {
    123456789: {
        "name": "Іваненко Олег",
        "subject": "Математика",
        "schedule": {
            "Понеділок": "8-А, 8-Б",
            "Вівторок": "9-А",
            "Середа": "11-Г",
            "Четвер": "10-А",
            "Пʼятниця": "8-А"
        }
    }
}


#  ХЕНДЛЕРИ
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Вітаю 👋\nОбери пункт меню:", reply_markup=menu)

@dp.message(lambda m: m.text == "🔔 Розклад дзвінків")
async def bells(message: types.Message):
    await message.answer(BELLS)

@dp.message(lambda m: m.text == "📁 Корисні матеріали")
async def materials(message: types.Message):
    await message.answer(f"✅ Корисні матеріали:\n{GOOGLE_DRIVE_LINK}")

@dp.message(lambda m: m.text == "📰 Новини ліцею")
async def news_handler(message: types.Message):
    await message.answer("\n".join(NEWS))

@dp.message(lambda m: m.text == "👨‍🏫 Кабінет вчителя")
async def teacher_cabinet(message: types.Message):
    teacher = teachers.get(message.from_user.id)
    if not teacher:
        await message.answer("❌ Доступ заборонений")
        return

    await message.answer(
        f"👨‍🏫 {teacher['name']}\n"
        f"📘 Предмет: {teacher['subject']}\n\n"
        "✏️ Редагування розкладу:\n"
        "✏️ Понеділок: 9-А, 10-Б"
    )

@dp.message(lambda m: m.text == "📅 Мій розклад")
async def my_schedule(message: types.Message):
    teacher = teachers.get(message.from_user.id)
    if not teacher:
        return

    text = "📅 Ваш розклад:\n\n"
    for day, lessons in teacher["schedule"].items():
        text += f"{day}: {lessons}\n"
    await message.answer(text)

@dp.message(lambda m: m.text.startswith("✏️"))
async def edit_schedule(message: types.Message):
    teacher = teachers.get(message.from_user.id)
    if not teacher:
        return

    try:
        data = message.text.replace("✏️", "").strip()
        day, value = data.split(":", 1)
        teacher["schedule"][day.strip()] = value.strip()
        await message.answer("✅ Розклад оновлено")
    except:
        await message.answer("❌ Невірний формат\n✏️ Понеділок: 9-А, 10-Б")

async def main():
    print("Бот працює на Render ✔️")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

#  ЛОКАЛЬНИЙ ЗАПУСК (POLLING)
# async def main_local():
#     print("Бот запущено локально ✔️")
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main_local())



