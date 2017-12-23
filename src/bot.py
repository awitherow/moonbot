#!/usr/bin/python
""" the bot package servers as a telegram adapter """
import telegram
import emoji
from config import telegram_token, telegram_chat_prod, telegram_chat_dev, env, kirby_bot_channel, cryptomumma, btc_tip_jar

TELLIE = telegram.Bot(token=telegram_token)

PROD_CHANNELS = [telegram_chat_prod, kirby_bot_channel, cryptomumma]
TEST_CHANNELS = [telegram_chat_dev]


def get_id_by_user(u):
    return {
        "azurikai": 247829509,
    }[u]


def build_info_template():
    moon_symbol = emoji.emojize(":full_moon:")
    crystal_ball_symbol = emoji.emojize(":crystal_ball:")

    message_text = moon_symbol + " Moon Room Resources " + moon_symbol + "\n"
    message_text += "- *FREE* Trading Guide -> bit.ly/2vFCM5W \n"
    message_text += "- Roadmap -> bit.ly/2wOPi7Z \n"
    message_text += "- Website -> bit.ly/2wmfMLz\n"
    message_text += "- Report bugs! -> goo.gl/forms/CPOCGE86TwDrf1sr1\n"
    message_text += "- Request features! -> goo.gl/forms/bdHcPk5TsRH5roZL2\n\n"
    message_text += crystal_ball_symbol + \
        " Write @azurikai at any time. " + \
        crystal_ball_symbol + "\n"
    return text


def build_ad_template():
    rocket_symbol = emoji.emojize(":rocket:")
    chart_symbol = emoji.emojize(":chart_increasing:")
    lightning_symbol = emoji.emojize(":cloud_with_lightning:")

    text = emoji.emojize(chart_symbol + " *STABLE INVESTMENTS* \n")
    text += emoji.emojize(" - " + lightning_symbol +
                          " [$BUZZ](http://buzzcoin.info)! -> Innovation in Energy \n\n")

    text += emoji.emojize(rocket_symbol +
                          " *SUPPORT DEVELOPMENT WITH:* \n")

    text += "BTC: `" + btc_tip_jar + "`\n"

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


def send_message(text, user=None, disable_link_preview=True, typ="public"):
    """ send_message sends a text message to the environment variable chat id,
        in markdown
    """

    if typ is "public":
        channels = PROD_CHANNELS

        if env == "test":
            channels = TEST_CHANNELS

        for channel in channels:
            TELLIE.send_message(chat_id=channel, text=text,
                                parse_mode="Markdown",
                                disable_web_page_preview=disable_link_preview)

    if typ is "private":
        chat_id = get_id_by_user(user)
        TELLIE.send_message(parse_mode="Markdown", text=text,
                            disable_link_preview=False, chat_id=chat_id)


def build_rating_template(scores, title):
    """ build_rating_template builds and returns a
        text message for twitter based coin score ratings
    """

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
