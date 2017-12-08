#!/usr/bin/python
""" the archivist deals with archived data in the databases """
import os
from operator import itemgetter

import postgres
from rex import Client
from helpers import get_time_now, find
from dateutil.parser import parse as parse_date
from datetime import timedelta, datetime
from config import env
from helpers import get_time_now
from datetime import timedelta
CWD = os.getcwd()


def get_cutoff(x):
    now = get_time_now(naive=False)
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
    if last_op is not None:
        # TODO: Store duruation in database
        start = int(last_op["main_start"])
        end = int(last_op["main_end"])
        duration = abs(start - end)
        print("[INFO] last moon_call duration was " +
              str(duration) + " seconds.")
        return duration

    return 0


def get_last_twitter_scan_duration():
    """ get_last_twitter_scan_duration returns the official twitter call
        duration
    """

    last_op = postgres.get_last_twitter_scan_duration()
    if last_op is not None:
        return last_op["duration"]

    return 0


def get_last_scores(tf):
    """ get_last_scores returns the last scores from the moon call based on the timeframe"""

    last_op = postgres.get_moon_call_operations()
    if last_op is not None:
        if tf == "day":
            return last_op["daily_coins"]

    return []
