import telebot
import requests
import random

API_key=("1973829382:AAEPzeQgP4z-m9jEaE7vddr7aKon18QQQ3w")
bot = telebot.TeleBot(API_key)


@bot.message_handler(commands= ["greet","hello",'hi','hey'])
def greet(message):
    ls = ['hello! there my name is jabby type /heyjabby to know more']
    bot.reply_to(message,random.choice(ls))

@bot.message_handler(commands= ["heyjabby"])
def money (message):
  bot.send_message(message.chat.id,"hello there for joke send /joke , for coffee send /coffee and for dog send /dog ")

@bot.message_handler(commands = ["coffee"])
def coffee(message):
    x = requests.get('https://coffee.alexflipnote.dev/random.json').json()
    url = x['file']
    bot.send_photo(message.chat.id, url)

@bot.message_handler(commands= ["joke"])
def joke (message):
    x = requests.get("https://v2.jokeapi.dev/joke/Any").json()
    joke = x["setup" ]+ "   \n " + x["delivery"]
    bot.send_message(message.chat.id,joke)

@bot.message_handler(commands = ["dog"])
def dog(message):
    x = requests.get('https://random.dog/woof.json').json()
    url = x['url']
    bot.send_photo(message.chat.id, url)

bot.polling()
