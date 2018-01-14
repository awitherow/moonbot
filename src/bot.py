#!/usr/bin/python
""" the bot package servers as a telegram adapter """
import telegram
import emoji
import math
import time
from datetime import datetime
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, env, kirby_bot_channel, telegram_chat_prod_vip

TELLIE = telegram.Bot(token=telegram_token)

FREE_PROD_CHANNELS = [telegram_chat_prod]
PAID_PROD_CHANNELS = [kirby_bot_channel, telegram_chat_prod_vip]
TEST_CHANNELS = [telegram_chat_dev]


def delivery_boy(text, channels):
    """ sends a message to an array of channels"""
    for channel in channels:
        TELLIE.send_message(chat_id=channel, text=text,
                            parse_mode="Markdown", disable_web_page_preview=True)


def build_info_template():
    moon_symbol = emoji.emojize(":full_moon:")
    crystal_ball_symbol = emoji.emojize(":crystal_ball:")

    text = moon_symbol + " Moon Room Resources " + moon_symbol + "\n"
    text += "- *FREE* Trading Guide -> bit.ly/2vFCM5W \n"
    text += "- Roadmap -> bit.ly/2wOPi7Z \n"
    text += "- Website -> bit.ly/2wmfMLz\n"
    text += "- Report bugs! -> goo.gl/forms/CPOCGE86TwDrf1sr1\n"
    text += "- Request features! -> goo.gl/forms/bdHcPk5TsRH5roZL2\n\n"
    text += crystal_ball_symbol + \
        " Write @azurikai at any time. " + \
        crystal_ball_symbol

    return text


def build_ad_template():
    rocket_symbol = emoji.emojize(":rocket:")
    chart_symbol = emoji.emojize(":chart_increasing:")
    lightning_symbol = emoji.emojize(":cloud_with_lightning:")

    text = emoji.emojize(chart_symbol + " *STABLE INVESTMENTS* \n")
    text += emoji.emojize(" - " + lightning_symbol +
                          " [$BUZZ](http://buzzcoin.info)! -> Innovations in Smart Energy Contracts, Save the Bees Project!\n\n")

    text += rocket_symbol + rocket_symbol + \
        rocket_symbol + rocket_symbol + "\n"
    text += "You are currently using the *FREE* version of MOONBOT.\n"
    text += "This version posts only Twitter scoring every 4 hours.\n"
    text += "Want access to hourly posting and future roadmap items? \n\n"
    text += "[Sign up TODAY for VIP Access!](http://bit.ly/2D4y9XC)\n\n"
    text += rocket_symbol + rocket_symbol + rocket_symbol + rocket_symbol

    return text


def generate_and_post_message(hourly, daily):
    """
        generates and posts a message using the build template and send message functions
        accepts hourly, daily scores
        - scores currently are expected to be of shape [{ symbol: string, score: int }]
        - scores will evolve to coins array => [{ symbol: string, scores: { medium: int }}]
        -- medium being "twitter", "reddit", "google", etc.
    """

    text = build_rating_template(hourly, "Hourly Twitter Hype") + "\n"

    if daily:
        daily_text = build_rating_template(daily, "Daily Twitter Hype")
        text += daily_text + "\n"

    send_message(text=text)


def send_new_coin_notification(symbol):
    """ lets developers know there is a new coin that needs to get some infos """

    text = "New coin " + symbol + " needs infos!"
    delivery_boy(text, TEST_CHANNELS)


def send_message(text, category="data"):
    """ send_message sends a text message to the environment variable chat id, in markdown """

    if env == "test":
        delivery_boy(text, TEST_CHANNELS)
        return

    now = time.localtime(time.time())

    if env == "prod":
        if category == "data":
            if int(now.tm_hour) % 4 == 0:
                delivery_boy(text, FREE_PROD_CHANNELS)

            delivery_boy(text, PAID_PROD_CHANNELS)

        if category == "ad":
            delivery_boy(text, FREE_PROD_CHANNELS)

        if category == "info":
            delivery_boy(text, FREE_PROD_CHANNELS)
            delivery_boy(text, PAID_PROD_CHANNELS)


def build_rating_template(scores, title):
    """ build_rating_template builds and returns a text message for twitter based coin score ratings """

    message = emoji.emojize("*:bird:" + title + ":bird: *\n")
    for market in scores:
        symbol = market["symbol"]

        # TODO: sentiment analysis
        # - ensure length is minus one to account for negative symbol
        # - if negative use skulls.
        birds = len(str(market["score"]))
        lit_meter = ""

        for _ in range(birds):
            lit_meter += emoji.emojize(":bird:")

        message += "- [$" + symbol + \
            "](https://twitter.com/search?f=tweets&vertical=default&q=%24" + \
            symbol + ") Score => " + lit_meter

        if "name" in market:
            message += " ::: [Research](https://coinmarketcap.com/currencies/" + \
                market["name"] + ")"

        message += " | [Analyze](https://www.tradingview.com/chart/?symbol=BITTREX:" + \
            market["symbol"] + "BTC)"

        message += " | [Trade](https://bittrex.com/Market/Index?MarketName=BTC-" + \
            market["symbol"] + ")"

        message += "\n"

    return message
