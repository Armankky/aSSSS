import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
from aiogram import Router
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
db_file = "database.json"

# بارگذاری دیتابیس
def load_db():
    if not os.path.exists(db_file):
        return {}
    with open(db_file, "r") as f:
        return json.load(f)

# ذخیره دیتابیس
def save_db(data):
    with open(db_file, "w") as f:
        json.dump(data, f)

# هندلر دریافت شماره تلفن
@router.message(F.contact)
async def handle_contact(message: Message):
    user_id = str(message.from_user.id)
    phone_number = message.contact.phone_number

    db = load_db()
    db[user_id] = phone_number
    save_db(db)

    await message.answer("شماره شما با موفقیت ذخیره شد.", reply_markup=ReplyKeyboardRemove())

# هندلر دریافت /start
@router.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="ارسال شماره 📱", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("برای ذخیره شماره، لطفاً شماره خود را ارسال کنید:", reply_markup=kb)

# هندلر دریافت آیدی عددی
@router.message(F.text.regexp(r'^\d+$'))
async def get_phone_by_id(message: Message):
    user_id = message.text.strip()
    db = load_db()
    phone_number = db.get(user_id)

    if phone_number:
        await message.answer(f"📞 شماره کاربر {user_id}: <code>{phone_number}</code>")
    else:
        await message.answer("❌ شماره‌ای برای این آیدی ذخیره نشده است.")

# راه‌اندازی ربات
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
