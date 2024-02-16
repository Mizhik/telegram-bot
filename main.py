import telebot
from telebot import types
import requests
import json
import webbrowser

bot = telebot.TeleBot("6875628949:AAECqbTHSZbEl6zhXppz3j4OzCtH2CQIp-s")
API = "aab1fb0cd6f961b2d87c23ae2c01ab64"

@bot.message_handler(commands=['github'])
def site(message):
    webbrowser.open("https://github.com/Mizhik/telegram-bot")


@bot.message_handler(commands=['weather'])
def weather_bot(message):
    bot.send_message(message.chat.id, "Hello! Enter your city:")

@bot.message_handler(commands=["start", "back"])
def start(message):
    file = open("./photo.jpeg", 'rb')
    bot.send_message(message.chat.id, "Hello! I'a Vlad\nThis bot for test\n")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Weather in my city", callback_data="weather")
    btn2 = types.InlineKeyboardButton("Name", callback_data="name")
    btn3 = types.InlineKeyboardButton("ID", callback_data="id")
    markup.row(btn1,btn2,btn3)
    bot.send_photo(message.chat.id,file,reply_markup=markup)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'weather':
        bot.send_message(callback.message.chat.id, "Enter your city:")
        @bot.message_handler(content_types=['text'])
        def get_weather(message):
            city = message.text.strip().lower()
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
            if res.status_code == 200:
                data = json.loads(res.text)
                temp = data['main']['temp']

                image = "sun.jpg" if temp > 5.0 else 'snow.jpg'
                file = open('./' + image, 'rb')
                bot.send_photo(message.chat.id, file)

                bot.reply_to(message,f"Now weather: {temp}")
            else:
                bot.reply_to(message,f"{city} - Сity does not exist")
    elif callback.data == 'name':
        bot.send_message(callback.message.chat.id, callback.message.chat.first_name)
    elif callback.data == 'id':
        bot.send_message(callback.message.chat.id, callback.message.chat.username)

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, message)

if __name__ == "__main__":        
    bot.infinity_polling()