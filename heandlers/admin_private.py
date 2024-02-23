from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_product, orm_get_products

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard



admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Додати товар",
    "Асортимент",
    placeholder="Виберіть дію",
    sizes=(2,),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Що хочите зробити?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Асортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}\
                    <strong>\n{product.description}\nЦіна: {round(product.price,2)}',
        )
    await message.answer("ОК, ось список товарі")



#Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введіть назву заново:',
        'AddProduct:description': 'Введіть опис заново:',
        'AddProduct:price': 'Введіть ціну заново:',
        'AddProduct:image': 'Цей state останній...',
    }

@admin_router.message(StateFilter(None),F.text == "Додати товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введіть назву товару", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'),Command("відміна"))
@admin_router.message(StateFilter('*'),F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Дія відмінена", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'),Command("повернутися"))
@admin_router.message(StateFilter('*'),F.text.casefold() == "повернутися")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer("Попереднього кроку немає, введіть назву товару або напишіть 'відміна'")
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, ви повернулися до минулого кроку \n {AddProduct.texts[previous.state]}")
            return
        previous = step

@admin_router.message(AddProduct.name,F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть опис товару")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели недопустимі данні, введіть назву товару")


@admin_router.message(AddProduct.description,F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description = message.text)
    await message.answer("Введіть ціну товару")
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price = message.text)
    await message.answer("Завантажити зображення товару")
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.image,F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    
    await state.update_data(image = message.photo[-1].file_id)
    data = await state.get_data()
    try:
        await orm_add_product(session,data)
        await message.answer("Товар додано", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(
        f"Помилка: \n{str(e)}\n", reply_markup=ADMIN_KB)
        await state.clear()