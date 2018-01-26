#!/usr/bin/python
""" the archivist deals with archived data in the databases """
from operator import itemgetter
from datetime import timedelta

import postgres
from helpers import get_time_now


def get_cutoff(timeframe):
    """ creates a cuttoff time based on a timeframe, currentls supports 'days'"""
    now = get_time_now(naive=False)
    day_delta = timedelta(hours=24)

    return {
        "day": now - day_delta,
    }[timeframe]


def get_score_history(timeframe):
    """ gets the score history for all coins, returning top 3 for the respective timeframe """

    cutoff = get_cutoff(timeframe)
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


def get_last_scores(timeframe):
    """ get_last_scores returns the last scores from the moon call based on the timeframe"""

    last_op = postgres.get_moon_call_operations()

    if last_op is not None:
        if timeframe == "day":
            return last_op["daily_coins"]

    return []
