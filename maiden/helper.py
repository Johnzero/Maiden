# encoding: utf-8

from datetime import datetime, date
import functools, time
try:
    from json import dumps
except ImportError:
    from simplejson import dumps

from flask import Response

#@jsonify
#def index():
#    return {'foo': 'bar', 'baz': [1,2,3]}


def to_timestamp(date):
    return int(time.mktime(date.timetuple())) * 1000

def jsonify(f):
    def inner(*args, **kwargs):
        return Response(dumps(f(*args, **kwargs)), mimetype='application/json')
    return inner

def keep_login_url(func):
    """
    Adds attribute g.keep_login_url in order to pass the current
    login URL to login/signup links.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        g.keep_login_url = True
        return func(*args, **kwargs)
    return wrapper


def timesince(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    
    if default is None:
        default = '刚刚'

    now = datetime.now()
    diff = now - dt
    periods = (
        (diff.days / 365, "年"),
        (diff.days / 30,  "月"),
        (diff.days / 7,  "周"),
        (diff.days, "天"),
        (diff.seconds / 3600,  "小时"),
        (diff.seconds / 60, "分钟"),
        (diff.seconds, "秒钟"),
    )

    for period, name in periods:
        if period > 0:
            return "%d %s 前" % (period, name)

    return default
