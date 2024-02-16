import telebot
from telebot import types
import requests
import json
import webbrowser
import sqlite3

bot = telebot.TeleBot("6875628949:AAECqbTHSZbEl6zhXppz3j4OzCtH2CQIp-s")
API = "aab1fb0cd6f961b2d87c23ae2c01ab64"
#кнопки та функціонал для них
'''
name = None

@bot.message_handler(commands=['database'])
def data_base(message):
    conn = sqlite3.connect('telebot.sql')
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Hello! For registering enter your name:")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Enter password:")
    bot.register_next_step_handler(message, user_password)

def user_password(message):
    password = message.text.strip()

    conn = sqlite3.connect('telebot.sql')
    cur = conn.cursor()
    
    cur.execute('INSERT INTO users(name, pass) VALUES("%s", "%s")' %(name,password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("User list", callback_data='users'))
    bot.send_message(message.chat.id, "User is registered", reply_markup=markup)

@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    conn = sqlite3.connect('telebot.sql')
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Name: {el[1]}\nPassword: {el[2]}\n {"-"*25}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)
#Функціонал + візуал
    
@bot.message_handler(commands=['github'])
def site(message):
    webbrowser.open("https://github.com/Mizhik/telegram-bot")

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Go")
    markup.row(btn1)
    btn2 = types.KeyboardButton("Delete")
    btn3 = types.KeyboardButton("Change")
    markup.row(btn2,btn3)
    file = open("./photo.jpeg", 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    #bot.send_message(message.chat.id, "Hello", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "Go":
        bot.send_message(message.chat.id, "GitHub")
    elif message.text == "Delete":
        bot.send_message(message.chat.id, "Delete")

# def main(message):
#     bot.send_message(message.chat.id, f"Hello,{message.from_user.first_name} @{message.from_user.username}")


@bot.message_handler()
def info(message):
    if message.text.lower() == "hello":
        bot.send_message(message.chat.id, f"Hello,{message.from_user.first_name} @{message.from_user.username}")
    elif message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Go!", url='https://web.telegram.org/a/#751859689')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Delete", callback_data = 'delete')
    btn3 = types.InlineKeyboardButton("Change", callback_data= 'edit')
    markup.row(btn2,btn3)
    bot.reply_to(message,"Nice picture", reply_markup = markup)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)
'''
#погода з сайту, отримуємо назву і виводимо через json данні
'''
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Enter your city:")


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
'''
#Щось трохи питався
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
        bot.send_message(callback.message.chat.id, "Vlad")
    elif callback.data == 'id':
        bot.send_message(callback.message.chat.id, "id")
if __name__ == "__main__":        
    bot.infinity_polling()
