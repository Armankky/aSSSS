from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import asyncio
from config import BOT_TOKEN
from database import save_user, get_phone_by_user_id

# ساخت ربات و Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    # کیبورد برای درخواست شماره کاربر
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 ارسال شماره من", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("لطفا روی دکمه زیر کلیک کنید تا شماره خود را ارسال کنید 👇", reply_markup=kb)


@dp.message(F.contact)
async def contact_handler(message: types.Message):
    contact = message.contact
    user_id = contact.user_id
    phone_number = contact.phone_number

    save_user(user_id, phone_number)

    await message.answer(f"شماره شما ثبت شد:\n👤 <b>User ID:</b> <code>{user_id}</code>\n📱 <b>Phone:</b> <code>{phone_number}</code>")


@dp.message(F.text.startswith("/getphone"))
async def get_phone_handler(message: types.Message):
    try:
        _, user_id_str = message.text.split()
        user_id = int(user_id_str)
        phone = get_phone_by_user_id(user_id)
        if phone:
            await message.reply(f"📞 شماره کاربر:\n<code>{phone}</code>")
        else:
            await message.reply("❌ شماره‌ای برای این آیدی پیدا نشد.")
    except:
        await message.reply("❗ لطفاً دستور را به‌درستی وارد کنید:\n/getphone user_id")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
