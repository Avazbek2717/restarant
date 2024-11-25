from aiogram import Bot, Dispatcher, types 
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio


bot = Bot(token = "7574149033:AAFfoVm4ysgSKk3kNoeTlyR-CZwS9wEbkMU")


dp = Dispatcher() #boshqaruvchi





@dp.message(CommandStart())
async def start(message: Message):
    await message.reply(text=f"{message.from_user.first_name}\nAssalomu alaykum botimizga hush kelibsiz\nBu bot matndagi hamma belgilani sanaydi.")
    await bot.send_message(chat_id=5167032738, text=f'{message.from_user.username} sizning botingizga start bosdi')

# @dp.message()
# async def echo(message: Message):
#     await message.reply(text=message.text)

@dp.message()
async def count_l(message: Message):
    t =  message.text
    numbers = 0
    words  = 0
    signs = 0
    space = 0
    for i in t:
        if str(i).isalpha():
            words = words +1
        if str(i).isdigit():
            numbers = numbers +1
        if not str(i).isalnum():
            signs =signs +1
        if str(i).isspace():
            space =space +1
    await message.reply(text=f"Matndagi raqamlar soni: {numbers}\nMatndagi harflar soni: {words}\nBelgilar soni: {signs}\nBo\'sh joylar soni: {space}")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())