# encoding: utf-8

"""
Created by J.W. on 2012-12-10.
Copyright (c) 2012 FUGUANG Industrial Co., Lmt.. All rights reserved.
"""

import os

def get_upload_folder():
    path = os.path.join(os.path.dirname(__file__), 'static', 'upload')
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(os.path.join(path, 'product'))
    return path


class DefaultConfig(object):
    """
    Default configuration for a newsmeme application.
    """

    DEBUG = True
    
    use_reloader = False
    
    SECRET_KEY = "zuSAyu3XRqGRvAg0HxsKX12Nrvf6Hk3AgZCWg1S1j9Y="

    SQLALCHEMY_DATABASE_URI = "sqlite:///maiden.db"
    
    DEBUG_TOOLBAR=True
    
    SQLALCHEMY_ECHO = False

    ADMINS = ()
    
    DEBUG_TB_INTERCEPT_REDIRECTS = False
	
    DEFAULT_MAIL_SENDER = ""

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    
    UPLOAD_FOLDER = get_upload_folder()
    EDITOR_UPLOAD_FOLDER = os.path.join(get_upload_folder(), 'temp')
    
    NEWS_PER_PAGE = 6
    RESELLER_PER_PAGE = 8
    PRODUCT_PER_PAGE = 12
    
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    

