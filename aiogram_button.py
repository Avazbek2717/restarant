from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

bot = Bot(token="7574149033:AAFfoVm4ysgSKk3kNoeTlyR-CZwS9wEbkMU")
dp = Dispatcher()

# Sanoqni boshlang'ich qiymati
c = 0

# Reply tugmalari yaratish
# def start_btns():
#     kbs = []
#     a = []
#     for i in range(10):
#         if len(a) < 3:
#             a.append(types.KeyboardButton(text=str(i)))
#         else:
#             kbs.append(a)
#             a = [types.KeyboardButton(text=str(i))]
#     kbs.append(a)
#     btns = types.ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)
#     return btns

# Inline tugmalarni yaratish
def inline_btns():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='+', callback_data='plus'),
        types.InlineKeyboardButton(text='0', callback_data='zero'),
        types.InlineKeyboardButton(text='-', callback_data='minus')
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(text='Assalomu alaykum, botimizga xush kelibsiz!')
    await message.answer(text=f'Sanoq: {c}', reply_markup=inline_btns(),)


@dp.callback_query()
async def callback_ansswear(callback: types.CallbackQuery):
    global c
    if callback.data == 'plus':
        c += 1
        await callback.answer(text='+')
    elif callback.data == 'minus':
        c -= 1
        await callback.answer(text='-')
    elif callback.data == 'zero':
        c = 0
        await callback.answer(text='0')
        

    await callback.message.edit_text(f'Sanoq: {c}', reply_markup=inline_btns())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


