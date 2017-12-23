#!/usr/bin/python
""" the helpers package contains help functions for the application """
import os
from datetime import datetime
import errno
import pytz


def find_date_in_string(str):
    # https://stackoverflow.com/questions/3276180/extracting-date-from-a-string-in-python
    return None


def find(lst, key, value):
    """ finds a key by matching value in a list of dictionaries """
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic

    return False


def get_time_now(stringify=False, naive=True):
    """ returns a proper default UTC timezone now time. """

    now = datetime.utcnow()
    if naive:
        now = now.replace(tzinfo=pytz.UTC)

    if stringify:
        return now.strftime('%s')

    return now


def touch(fname, times=None):
    """ touches a file as you would do in bash. """

    with open(fname, 'a'):
        os.utime(fname, times)


def mkdir_p(path):
    """ makes diretory, recursively. """

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
