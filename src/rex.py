#!/usr/bin/python
"""
the rex package is a bittrex exchange adapter.
"""
import bittrex
from operator import itemgetter
from helpers import find
from config import env
from postgres import get_coin_info, add_coin_info
Rex = bittrex.Bittrex(api_key="", api_secret="")


# blacklist is where coins who have too much non crypto currency meaning go. sorry :(
blacklist = ["GLD", "1ST", "2GIVE", "EMC2"]


def get_cream(list_of_things):
    """ get_cream gets the top 40% of the pack, no dregs please. """

    return int(len(list_of_things) * 0.2)


def get_market_summaries():
    """
    get_market_summaries gets the top 40% highest volume market summaries for
    btc, eth and usdt based markets
    TODO: how can we automate the btc/eth/usdt lists into automated list generation based on the split[0] for the MarketName?
    """
    summaries = Rex.get_market_summaries()["result"]
    currencies = Rex.get_currencies()["result"]

    btc_summaries = []
    eth_summaries = []
    usdt_summaries = []

    for summary in reversed(sorted(summaries, key=itemgetter("Volume"))):
        market = summary["MarketName"].split("-")[0]
        coin = summary["MarketName"].split("-")[1]

        entry = {}
        entry["symbol"] = coin

        coin_info = find(currencies, "Currency", coin)

        if coin_info:
            entry["name"] = coin_info["CurrencyLong"].lower()

        if market == "BTC":
            btc_summaries.append(entry)

        if market == "ETH":
            eth_summaries.append(entry)

        if market == "USDT":
            usdt_summaries.append(entry)

        infos = get_coin_info(coin)
        if not infos:
            add_coin_info(entry)

    summaries = btc_summaries[:get_cream(btc_summaries)] + eth_summaries[:get_cream(
        eth_summaries)] + usdt_summaries[:get_cream(usdt_summaries)]

    # get rid of blacklist terms
    for blacklisted in blacklist:
        for summary in summaries:
            if summary["symbol"] == blacklisted:
                summaries.remove(summary)

    # ensure no duplicates
    final = []
    for i in summaries:
        if i not in final:
            final.append(i)

    if env == "test":
        return final[:5]

    return final
