from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from datetime import datetime

bot = Bot(token="7574149033:AAFfoVm4ysgSKk3kNoeTlyR-CZwS9wEbkMU")
dp = Dispatcher()

food_menu = [
    {"name": "Pizza", "price": "50,000 UZS"},
    {"name": "Burger", "price": "30,000 UZS"},
    {"name": "Salad", "price": "20,000 UZS"},
    {"name": "Lag'mon", "price": "40,000 UZS"},
    {"name": "Shashlik", "price": "25,000 UZS"},
    {"name": "Tea", "price": "5,000 UZS"},
    {"name": "Juice", "price": "15,000 UZS"}
]

class RegistrForm(StatesGroup):
    language = State()
    full_name = State()
    stol_raqami = State()
    ovqatlar = State()


def inline_button():
    inline_b = InlineKeyboardBuilder()
    inline_b.row(
        types.InlineKeyboardButton(text='   Uzb', callback_data='uz'),
        types.InlineKeyboardButton(text='   Rus', callback_data="ru"),
        types.InlineKeyboardButton(text='   Eng', callback_data="eng")
    )
    return inline_b.as_markup()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.reply(text="Tilni tanlang / Выберите язык / Choose language:", reply_markup=inline_button())
    await state.set_state(RegistrForm.language)


@dp.callback_query()
async def callback_language(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "uz":
        await state.update_data(language="uz")
        await callback.message.answer("Til o'rnatildi: O'zbek tili. \nIsmingizni kiriting:")
    elif callback.data == "ru":
        await state.update_data(language="ru")
        await callback.message.answer("Язык установлен: Русский. \nВведите ваше имя:")
    elif callback.data == "eng":
        await state.update_data(language="eng")
        await callback.message.answer("Language set: English. \nEnter your name:")
    await state.set_state(RegistrForm.full_name)
    await callback.answer()


def back_button(language="uz"):
    text = "Orqaga" if language == "uz" else "Назад" if language == "ru" else "Back"
    return KeyboardButton(text=text)


@dp.message(RegistrForm.full_name)
async def set_full_name(message: Message, state: FSMContext):
    full_name = message.text
    data = await state.get_data()
    language = data.get("language", "uz")
    await state.update_data(full_name=full_name)

    buttons = [[back_button(language)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        selective=True
    )

    text = {
        "uz": "Stol nomerini tanlang:",
        "ru": "Выберите номер стола:",
        "eng": "Select your table number:"
    }.get(language, "Stol nomerini tanlang:")
    await message.answer(text=text, reply_markup=keyboard)
    await state.set_state(RegistrForm.stol_raqami)


@dp.message(RegistrForm.stol_raqami)
async def set_stol_raqami(message: Message, state: FSMContext):
    stol_raqami = message.text
    data = await state.get_data()
    language = data.get("language", "uz")

    if message.text == ("Orqaga" if language == "uz" else "Назад" if language == "ru" else "Back"):
        text = {
            "uz": "Ismingizni qayta kiriting:",
            "ru": "Введите ваше имя снова:",
            "eng": "Enter your name again:"
        }.get(language, "Ismingizni qayta kiriting:")
        await message.answer(text=text)
        await state.set_state(RegistrForm.full_name)
        return

    if not stol_raqami.isdigit():
        text = {
            "uz": "Noto'g'ri stol raqami kiritdingiz. Raqamni qayta kiriting.",
            "ru": "Неверный номер стола. Попробуйте снова.",
            "eng": "Invalid table number. Please try again."
        }.get(language, "Noto'g'ri stol raqami kiritdingiz. Raqamni qayta kiriting.")
        return await message.answer(text=text)

    await state.update_data(stol_raqami=stol_raqami)

    buttons = [[KeyboardButton(text=f"{item['name']} - {item['price']}")] for item in food_menu]
    buttons.append([back_button(language)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Tanlang..." if language == "uz" else "Выберите..." if language == "ru" else "Choose..."
    )

    text = {
        "uz": "Ovqatlardan birini tanlang:",
        "ru": "Выберите одно из блюд:",
        "eng": "Select one of the dishes:"
    }.get(language, "Ovqatlardan birini tanlang:")
    await message.answer(text=text, reply_markup=keyboard)
    await state.set_state(RegistrForm.ovqatlar)


@dp.message(RegistrForm.ovqatlar)
async def select_food(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    if message.text in ["Zakazni yakunlash", "Завершить заказ", "Complete order"]:
        foods = data.get("selected_foods", [])
        food_prices = data.get("food_prices", [])
        stol_raqami = data["stol_raqami"]
        full_name = data['full_name']

        total_price = sum(food_prices)

        text = (
            f"Zakaz berilgan vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Ism: {full_name}\n"
            f"Stol raqami: {stol_raqami}\n"
            f"Buyurtma:\n" + "\n".join([f"- {food} - {price} UZS" for food, price in zip(foods, food_prices)]) +
            f"\n\nJami: {total_price} UZS\n\nRahmat! Buyurtmangiz qabul qilindi."
            if language == "uz"
            else f"Время заказа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Имя: {full_name}\n"
            f"Номер стола: {stol_raqami}\n"
            f"Заказ:\n" + "\n".join([f"- {food} - {price} UZS" for food, price in zip(foods, food_prices)]) +
            f"\n\nИтого: {total_price} UZS\n\nСпасибо! Ваш заказ принят."
            if language == "ru"
            else f"Order time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Name: {full_name}\n"
            f"Table number: {stol_raqami}\n"
            f"Order:\n" + "\n".join([f"- {food} - {price} UZS" for food, price in zip(foods, food_prices)]) +
            f"\n\nTotal: {total_price} UZS\n\nThank you! Your order has been accepted."
        )
        await message.answer(text=text, reply_markup=None)

        # Admin uchun xabar
        admin_text = (
            f"Yangi buyurtma qabul qilindi!\n\n"
            f"Ism: {full_name}\n"
            f"Stol raqami: {stol_raqami}\n"
            f"Buyurtmalar:\n" + "\n".join([f"- {food} - {price} UZS" for food, price in zip(foods, food_prices)]) +
            f"\n\nJami summa: {total_price} UZS\n"
            f"Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await bot.send_message(chat_id='5167032738', text=admin_text)

        await state.clear()

    else:
        selected_food = message.text.split(" - ")[0]
        selected_price = next(item['price'] for item in food_menu if item['name'] == selected_food)
        selected_price_int = int(selected_price.replace(" UZS", "").replace(",", ""))

        foods = data.get("selected_foods", [])
        food_prices = data.get("food_prices", [])

        foods.append(selected_food)
        food_prices.append(selected_price_int)
        await state.update_data(selected_foods=foods, food_prices=food_prices)

        zakaz_tugatish_button = KeyboardButton(
            text="Zakazni yakunlash" if language == "uz"
            else "Завершить заказ" if language == "ru"
            else "Complete order"
        )
        buttons = [[KeyboardButton(text=f"{item['name']} - {item['price']}")] for item in food_menu]
        buttons.append([zakaz_tugatish_button, back_button(language)])

        keyboard = ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            input_field_placeholder=(
                "Tanlang yoki zakazni yakunlang..." if language == "uz"
                else "Выберите или завершите заказ..." if language == "ru"
                else "Choose or complete your order..."
            )
        )

        text = (
            f"Sizning buyurtmalaringiz:\n"
            + "\n".join([f"- {food} -> {price}" for food, price in zip(foods, food_prices)])
            + "\n\nBuyurtmangizni yakunlash uchun 'Zakazni yakunlash' tugmasini bosing."
            if language == "uz"
            else f"Ваши заказы:\n"
            + "\n".join([f"- {food} - {price}" for food, price in zip(foods, food_prices)])
            + "\n\nНажмите 'Завершить заказ', чтобы закончить."
            if language == "ru"
            else f"Your orders:\n"
            + "\n".join([f"- {food} - {price}" for food, price in zip(foods, food_prices)])
            + "\n\nPress 'Complete order' to finish."
        )
        await message.answer(text=text, reply_markup=keyboard)




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
