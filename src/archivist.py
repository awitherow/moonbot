""" the archivist deals with archived data in the databases """
import os
from datetime import datetime, date
from operator import itemgetter

import db
from rex import Rex
from helpers import get_time_now, find
from config import env
CWD = os.getcwd()


def get_score_history(tf):
    """ gets the score history for all coins, returning top 3 for the respective tf """

    score_files = CWD + "/db/" + env + "/symbols/"
    symbol_score_dbs = os.listdir(score_files)

    now_timestamp = float(get_time_now(stringify=True))
    now = datetime.fromtimestamp(now_timestamp)

    scores = []

    for symbol_db_file in symbol_score_dbs:
        entry = {}
        symbol = symbol_db_file.split(".")[0]
        entry["symbol"] = symbol[1:]
        symbol_db = db.get(path="symbols", file_name=symbol)

        tf_entries = len(symbol_db)
        tf_score = 0

        for data in symbol_db:
            if "name" in data and "name" not in entry:
                entry["name"] = data["name"]

            if tf == "day":
                today = now.day
                entry_timestamp = float(data["created"])
                score_day = datetime.fromtimestamp(entry_timestamp).day

                if today == score_day:
                    tf_score += data["score"]

            if tf == "week":
                cal_week = date.fromtimestamp(now_timestamp).isocalendar()[1]
                score_week = date.fromtimestamp(
                    float(data["created"])).isocalendar()[1]

                if cal_week == score_week:
                    tf_score += data["score"]
        score = 0
        if tf_entries is not 0 and tf_score is not 0:
            score = tf_score / tf_entries

        if "name" not in entry:
            currencies = Rex.get_currencies()["result"]
            coin_info = find(currencies, "Currency", symbol[1:])

            if coin_info:
                entry["name"] = coin_info["CurrencyLong"].lower()

        entry["score"] = score
        if score:
            scores.append(entry)

    sorted_scores = sorted(scores, key=itemgetter("score"), reverse=True)
    return sorted_scores[:3]


def get_twitter_res_time(time_range):
    """ get_twitter_res_time returns the logged average api response time for twitter """

    moon_call_ops = db.get(path="operations", file_name="moon_call")
    sorted_ops = sorted(moon_call_ops, key=itemgetter("_init"), reverse=True)

    res_time = 0

    if sorted_ops is not None:
        if time_range == "last":
            last_op = sorted_ops[0]

            if last_op:
                start = int(last_op["twitter_search_start"])
                end = int(last_op["twitter_search_end"])
                last_twitter_call_seconds = abs(start - end)
                res_time += last_twitter_call_seconds
                print "[INFO] last twitter response time was " + str(last_twitter_call_seconds) + " seconds."

        if time_range == "average" and sorted_ops is not None:
            durations = 0

            for operation in sorted_ops:
                start = int(operation["twitter_search_start"])
                end = int(operation["twitter_search_end"])
                durations += abs(start - end)

            res_time += durations / len(sorted_ops)
            print "[INFO] average twitter response time " + res_time + " seconds."

    return res_time


def get_moon_call_res_duration():
    """ get_moon_call_res_duration returns the moon call duration"""

    moon_call_ops = db.get(path="operations", file_name="moon_call")
    sorted_ops = sorted(moon_call_ops, key=itemgetter("_init"), reverse=True)

    moon_call_duration = 0

    if sorted_ops is not None:
        last_op = sorted_ops[0]

        if last_op:
            start = int(last_op["_init"])
            end = int(last_op["_end"])
            duration = abs(start - end)
            moon_call_duration += duration
            print "[INFO] last moon_call duration was " + str(duration) + " seconds."

    return moon_call_duration
