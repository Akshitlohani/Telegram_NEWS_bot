import telebot
import requests
import random


API_key = ""  # Add your own TELEGRAM API KEY inside " "
bot = telebot.TeleBot(API_key)


@bot.message_handler(
    commands=[
        "greet",
        "hello",
        "hi",
        "hey",
    ]
)
def greet(message):
    ls = ["hello! there my name is jabby type /heybot to know more"]
    bot.reply_to(message, random.choice(ls))


@bot.message_handler(commands=["heybot"])
def money(message):
    bot.send_message(
        message.chat.id,
        "hello there for joke send /joke, for coffee send /coffee, for dog send /dog, and for news send /news",
    )


@bot.message_handler(commands=["joke"])
def joke(message):
    x = requests.get("https://v2.jokeapi.dev/joke/Any").json()
    joke = x["setup"] + "   \n " + x["delivery"]
    bot.send_message(message.chat.id, joke)


@bot.message_handler(commands=["news"]) # refer to https://newsapi.org/
def news(message):
    news_url = ""   # Replace with the actual news API URL. 
    response = requests.get(news_url).json()
    articles = response["articles"]

    for article in articles:
        title = article["title"]
        description = article["description"]
        content = article["content"]
        news = f"{title}\n\nDescription: {description}\n\nContent: {content}"

        # Split the news into multiple messages if it exceeds the character limit
        while news:
            message_text = news[
                :4096
            ]  # Take a chunk of the news up to the character limit
            bot.send_message(message.chat.id, message_text)
            news = news[4096:]  # Remove the sent chunk from the remaining news


@bot.message_handler(commands=["coffee"])
def coffee(message):
    x = requests.get("https://coffee.alexflipnote.dev/random.json").json()
    url = x["file"]
    bot.send_photo(message.chat.id, url)


@bot.message_handler(commands=["dog"])
def dog(message):
    x = requests.get("https://random.dog/woof.json").json()
    url = x["url"]
    bot.send_photo(message.chat.id, url)


bot.polling()
