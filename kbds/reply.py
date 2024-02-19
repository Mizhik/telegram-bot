from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Menu'),
            KeyboardButton(text='Creator'),
        ],
        [
            KeyboardButton(text='Payment'),
            KeyboardButton(text='Shipping'),
        ] 
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose button >>>"
)

del_kb = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Menu'),
    KeyboardButton(text='Creator'),
    KeyboardButton(text='Payment'),
    KeyboardButton(text='Shipping'),
)
start_kb2.adjust(2,2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text='About'))

test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Створити опитування", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text = 'Надіслати номер', request_contact=True),
            KeyboardButton(text = 'Надіслати локацію', request_location=True),
        ],
    ],
    resize_keyboard=True,
)