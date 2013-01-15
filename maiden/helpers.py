# encoding: utf-8
"""
helpers.py

Created by J.W. on 2012-12-10.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

import re
import urlparse
import functools

from datetime import datetime
import sys, os, uuid, simplejson as json

from flask import current_app, g, Response

from maiden.extensions import cache

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def jsonify(f):
    """返回json"""
    def inner(*args, **kwargs):
        return Response(json.dumps(f(*args, **kwargs)), mimetype='application/json')
    return inner

#@app.context_processor
#def active_processor():
#    def page_active(code_list, path):
#        base_name = os.path.basename(path)
#        return base_name in code_list
#    return dict(page_active=page_active)


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


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. From http://flask.pocoo.org/snippets/5/"""
    result = []
    for word in _punct_re.split(text.lower()):
        #word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))


cached = functools.partial(cache.cached,
                           unless= lambda: g.user is not None)

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


def domain(url):
    """
    Returns the domain of a URL e.g. http://reddit.com/ > reddit.com
    """
    rv = urlparse.urlparse(url).netloc
    if rv.startswith("www."):
        rv = rv[4:]
    return rv
