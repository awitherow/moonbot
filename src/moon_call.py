#!/usr/bin/python
"""
the main package runs the main functionalities of the program
- moon_call is a function to call moon shots on market symbols
"""
from operator import itemgetter
from archivist import get_moon_call_res_duration, get_last_scores, get_score_history
from helpers import time_now
from bot import generate_and_post_message
from postgres import add_twitter_score, add_operations_log, clean_old_entries
import twit
import rex
import logician


def moon_call():
    """ call hot shots on market symbols """

    op = {}
    op["main_start"] = time_now(stringify=True)

    print("[INFO] Starting moon_call at " + op["main_start"])

    summaries = rex.get_market_summaries()
    # TODO: set up separated twitter scores, reddit scores. overlap scores?
    scores = []

    print("[INFO] Searching Twitter for BTRX symbol high volume list...")
    op["twitter_search_start"] = time_now(stringify=True)

    avg_res = get_moon_call_res_duration()

    print("[INFO] Scoring " + str(len(summaries)) + " coins...")
    # get and score relevant tweets per symbol.
    for i in summaries:
        entry = i
        entry["created"] = time_now(stringify=True)

        coin_symbol = "$" + i["symbol"]

        # search twitter
        tweets = twit.search(coin_symbol)
        score = logician.judge(tweets, stale_break=avg_res + 3200)

        # TODO: search reddit

        # if score sucks, go to next symbol
        if not score:
            continue

        entry["score"] = int(score)
        add_twitter_score(entry)
        scores.append(entry)

    op["twitter_search_end"] = time_now(stringify=True)

    # sort and find hottest trends
    sorted_scores = sorted(scores, key=itemgetter("score"), reverse=True)
    hourly_top_scores = sorted_scores[:5]

    print("[INFO] Preparing message templates...")

    daily_top_scores = get_score_history(tf="day")

    # track the daily coins for each call
    op["daily_coins"] = []
    for coin in daily_top_scores:
        op["daily_coins"].append(coin["symbol"])

    # ensure that we are not unnecessarily sending daily/ block
    last_daily = get_last_scores("day")

    day_matches_last_moon_call = False
    if last_daily is not None:
        day_matches_last_moon_call = last_daily == op["daily_coins"]

    if day_matches_last_moon_call:
        daily_top_scores = []

    # post to telegram
    op["send_message_start"] = time_now(stringify=True)
    generate_and_post_message(hourly_top_scores, daily_top_scores)
    op["send_message_end"] = time_now(stringify=True)

    print("[INFO] Moon call complete, message sent at " +
          time_now(stringify=True))

    op["main_end"] = time_now(stringify=True)
    add_operations_log(op)
    clean_old_entries()

    print("[INFO] Sleeping now for one hour...\n\n")


moon_call()
