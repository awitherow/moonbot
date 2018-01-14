#!/usr/bin/python
""" the config package works with environment variables """
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

if "heroku" not in environ:
    env = join(dirname(__file__), "../.env")
    load_dotenv(env)

# telegram bot
telegram_token = environ["bot_api_token"]
telegram_chat_prod = environ["telegram_chat_prod"]
telegram_chat_dev = environ["telegram_chat_dev"]
kirby_bot_channel = environ["kirby_bot_channel"]
telegram_chat_prod_vip = environ["telegram_chat_prod_vip"]

# bittrex api
rex_api_key = environ["bittrex_api_key"]
rex_api_secret = environ["bittrex_api_secret"]

# twitter
twitter_consumer_key = environ["twitter_consumer_key"]
twitter_consumer_secret = environ["twitter_consumer_secret"]
twitter_access_token = environ["twitter_access_token"]
twitter_access_secret = environ["twitter_access_secret"]


# environment
env = environ["ENV"]
