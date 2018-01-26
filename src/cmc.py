#!/usr/bin/python
""" the cmc package servers as a coinmarketcap adapter """

import coinmarketcap
import postgres

TICKER_GETTER = coinmarketcap.Market()


def get_all_coins():
    """ get all coin tickers from coinmarketcap """

    all_tickers = TICKER_GETTER.ticker(limit=0)
    past_tickers = postgres.get_past_tickers()

    # TODO: first -> check ticker lengths, if equal
    # - if past_tickers is empty, return from entire function.
    # - find "new" based on id comparison
    # - send message to channel about new coin

    # sort all tickers by rank
    # compare one by one of each in past_tickers
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

    # TODO: first -> after all, for each ticker in all_tickers, store to past_tickers if updated.
