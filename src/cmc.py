#!/usr/bin/python
""" the cmc package servers as a coinmarketcap adapter """

from operator import itemgetter

import coinmarketcap
import helpers
import postgres
import bot

TICKER_GETTER = coinmarketcap.Market()


def store_tickers(new):
    """ stores all coinmarketcap tickers from the last hour """
    # simply store all tickers
    postgres.wipe_cmc_history()

    for ticker in new:
        postgres.add_cmc_data(ticker)


def analyze_coin_marketcap_tickers():
    """
        analyze and take action upon new tickets compared to old tickers tickers from coinmarketcap
        1) if there are new coins compared to the old list, sent out notification about new coins to paid channels
    """

    new = TICKER_GETTER.ticker(limit=0)
    past = postgres.get_past_tickers()

    new = sorted(new, key=itemgetter("rank"), reverse=True)
    past = sorted(past, key=itemgetter("rank"), reverse=True)

    if past is not None:
        if len(past) == len(all):
            new_coins = []

            for tick in past:
                match = helpers.find(new, "id", tick["id"])

                if match is None:
                    new_coins.append(match)

            if len(new_coins):
                # 1) builds and sends new coins template
                bot.build_cmc_new_coins_template(new_coins)

            # compare one by one of each in past
            # TODO: second -> if 1) rank has increased by X%, add to list of increased ranking percentage
            # - what X% is good to catch changes in top 10 that are "huge",
            # - but also in top 100, top 250, etc that are "important"
            # - also what is the limit? do we check all?
            # - perhaps scaling X, 1-10, 10-25, 25-100, 100-250, 250+?
            # TODO: third -> using same rules above, check percentages for 2) hourly 3) daily, 4) weekly percentage changes
            # TODO: fourth ->: using same rules above, check 5) usd fluctuations.
            # once rank change complete, sent out a message with each of these listed out.

            # TODO: fifth ->
            # if same tickers are in more than 2 (or 3?) of the 5 above, create special
            # announcement how this one was in each of the list groups "high attention coins"

            # TODO: first -> after all, for each ticker in all_tickers, store to past if updated.

    # once parsed, analyzed and taken action upon, store tickers (deletes old ones, adds new ones)
    store_tickers(new)
