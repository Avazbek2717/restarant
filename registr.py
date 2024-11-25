


# from aiogram import Bot, Dispatcher, types 
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
# import asyncio
# from aiogram.fsm.state import StatesGroup,State
# from aiogram.fsm.context import FSMContext
# import re

# bot = Bot(token = "7574149033:AAFfoVm4ysgSKk3kNoeTlyR-CZwS9wEbkMU")


# dp = Dispatcher() #boshqaruvchi


# class RegistrForm(StatesGroup):
#     full_name = State()
#     phone_number = State()
#     course = State()
#     age = State()



# def chekc_cours_b():
#     butt = [[types.KeyboardButton(text='Backend')],[types.KeyboardButton(text='Fron end')],
#             [types.KeyboardButton(text= 'Dizaytan')]]
#     btns = types.ReplyKeyboardMarkup(keyboard=butt, resize_keyboard=True)
#     return btns



# # phone number uchun

# def check_phone(phone):
#     v = re.compile('^998[0-9]{9}')
#     return v.search(phone) is not None

# #age uchun


    



# @dp.message(CommandStart())
# async def start(message: Message, state: FSMContext):
#     await message.reply(text=f"{message.from_user.first_name}\nAssalomu alaykum botimizga hush kelibsiz\nro'yxatdan o'tish boshlandi: ")
#     await state.set_state(RegistrForm.full_name)

# @dp.message(RegistrForm.full_name)
# async def set_full_name(message: Message, state:FSMContext):
#     full_name  = message.text
#     await state.update_data(full_name=full_name)
#     await message.answer(text='Telefon raqamingizni kiriitng')
#     await state.set_state(RegistrForm.phone_number)

# @dp.message(RegistrForm.phone_number)
# async def set_phone_number(message:Message,state:FSMContext):
#     phone_number = message.text
#     if not check_phone(phone_number):
#         return await message.answer(text='siz notori raqam kriritingiz')
#     await state.update_data(phone_number = phone_number)
#     await message.answer(text='kurs nomini kiriting',reply_markup=chekc_cours_b())
#     await state.set_state(RegistrForm.course)

# @dp.message(RegistrForm.course)
# async def set_course(message:Message,state:FSMContext):

#     course = message.text

#     await state.update_data(course = course)
#     await message.answer(text='Yoshingizni kiriting')
#     await state.set_state(RegistrForm.age)

# @dp.message(RegistrForm.age)
# async def set_age(message:Message,state: FSMContext):
#     age = message.text
#     if not age.isdigit():
#         return await message.answer(text='Notori yosh kiritdingiz')
#     await state.update_data(age=age)
    
#     data = await state.get_data()
#     text = f"Siz kiritigan malumotlar: \nIsmi {data['full_name']} \nTel nomer {data['phone_number']}\nKurs nomi {data['course']} \nYoshi {data['age']}"
#     await message.answer(text=text)
#     await state.clear()











# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())