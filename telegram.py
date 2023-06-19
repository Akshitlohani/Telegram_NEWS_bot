import telebot
import requests
import random

API_key = ""  # Add your own TELEGRAM API KEY inside " ". Refer https://core.telegram.org/bots/tutorial
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
    ls = ["hello! type /heybot to know about the things that I can do for you"]
    bot.reply_to(message, random.choice(ls))


@bot.message_handler(commands=["heybot"])
def money(message):
    bot.send_message(
        message.chat.id,
        "Hello there! For a joke, send /joke. For coffee, send /coffee. For a dog picture, send /dog. And for news, send /news",
    )


@bot.message_handler(commands=["joke"]) # refer https://v2.jokeapi.dev/
def joke(message):
    joke_url = "https://sv443.net/jokeapi/v2/joke/Any"  # JokeAPI URL

    try:
        response = requests.get(joke_url).json()

        if response["type"] == "single":
            joke_text = response["joke"]
        elif response["type"] == "twopart":
            joke_setup = response["setup"]
            joke_delivery = response["delivery"]
            joke_text = f"{joke_setup}\n\n{joke_delivery}"
        else:
            raise KeyError("Invalid joke response")
    except (requests.RequestException, KeyError):
        bot.reply_to(message, "Sorry, I couldn't fetch a joke at the moment.")
        return

    bot.send_message(message.chat.id, joke_text)


@bot.message_handler(commands=["news"])
def request_article_count(message):
    bot.reply_to(message, "How many news articles would you like to receive?")
    bot.register_next_step_handler(message, process_article_count)


def process_article_count(message):
    try:
        article_count = int(message.text)

        if article_count <= 0:
            raise ValueError("Invalid article count")

        fetch_news(message, article_count)
    except ValueError:
        bot.reply_to(
            message, "Please enter a valid positive number for the article count."
        )


def fetch_news(message, article_count):
    news_url = ""  # Replace with the actual news API URL. Please refer to the given link https://newsapi.org/

    try:
        response = requests.get(news_url).json()
        articles = response["articles"]

        for i, article in enumerate(articles):
            if i >= article_count:
                break

            title = article["title"]
            description = article["description"]
            url = article["url"]
            news = f"{title}\n\n Description: {description}\n\n link to full Article: {url}"
            bot.send_message(message.chat.id, news)

    except (requests.RequestException, KeyError):
        bot.reply_to(message, "Sorry, I couldn't fetch the news at the moment.")


@bot.message_handler(commands=["coffee"])
def coffee(message):
    try:
        x = requests.get("https://coffee.alexflipnote.dev/random.json").json()
        url = x["file"]
        bot.send_photo(message.chat.id, url)
    except (requests.RequestException, KeyError):
        bot.reply_to(
            message,
            "Sorry, I couldn't fetch a coffee image at the moment. Try reducing the article count or come back later.",
        )
        return


@bot.message_handler(commands=["dog"])
def dog(message):
    try:
        x = requests.get("https://random.dog/woof.json").json()
        url = x["url"]
        bot.send_photo(message.chat.id, url)
    except (requests.RequestException, KeyError):
        bot.reply_to(message, "Sorry, I couldn't fetch a dog image at the moment.")
        return


bot.polling()
