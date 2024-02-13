import telebot
import webbrowser

bot = telebot.TeleBot("6875628949:AAECqbTHSZbEl6zhXppz3j4OzCtH2CQIp-s")

@bot.message_handler(commands=['github'])
def site(message):
    webbrowser.open("https://github.com/Mizhik/telegram-bot")

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, f"Hello,{message.from_user.first_name} @{message.from_user.username}")


@bot.message_handler()
def info(message):
    if message.text.lower() == "hello":
        bot.send_message(message.chat.id, f"Hello,{message.from_user.first_name} @{message.from_user.username}")
    elif message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")


bot.infinity_polling()
