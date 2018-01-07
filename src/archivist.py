#!/usr/bin/python
""" the archivist deals with archived data in the databases """
import os
from operator import itemgetter

import postgres
from helpers import time_now
from datetime import timedelta
CWD = os.getcwd()


def get_cutoff(x):
    now = time_now(naive=False)
    day_delta = timedelta(hours=24)

    return {
        "day": now - day_delta,
    }[x]


def get_score_history(tf):
    """ gets the score history for all coins, returning top 3 for the respective tf """

    cutoff = get_cutoff(tf)
    history = postgres.get_historical_twitter_scores(cutoff)
    if history is None:
        return []

    scores = []

    for record in history:
        exists = False
        # check scores and add score to existing score if it exists
        # break when exists so that we do not add unnecessary duplicaiton.
        for score in scores:
            if score["symbol"] == record["symbol"]:
                score["score"] += record["score"]
                exists = True
                break

        if not exists:
            scores.append(record)

    if scores is not None:
        scores = sorted(scores, key=itemgetter("score"), reverse=True)
        scores = scores[:5]

    return scores


def get_moon_call_res_duration():
    """ get_moon_call_res_duration returns the moon call duration"""

    last_op = postgres.get_moon_call_operations()

    moon_call_duration = 0

    if last_op is not None:
        start = int(last_op["main_start"])
        end = int(last_op["main_end"])
        duration = abs(start - end)
        moon_call_duration += duration
        print("[INFO] last moon_call duration was " +
              str(duration) + " seconds.")

    return moon_call_duration


def get_last_scores(tf):
    """ get_last_scores returns the last scores from the moon call based on the timeframe"""

    last_op = postgres.get_moon_call_operations()

    if last_op is not None:
        if tf == "day":
            return last_op["daily_coins"]

    return []
