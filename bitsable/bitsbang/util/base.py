#!/usr/bin/env python

import re
import random
import hashlib
import datetime

def encrypt(value, secret_key=None):
    """encrypt sha1"""
    hashed_value = hashlib.sha1(value).hexdigest()
    return hashed_value
    
def get_gmt(date):
    """get gmt date time format"""
    return date.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    
def random_str(length=6):
    strs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.sample(strs,length))
    
def set_cookies(handler, session_key):
    exp_date = get_gmt(datetime.datetime.now() + datetime.timedelta(days=30))
    handler.response.headers['Set-Cookie'] = 'bitsable-session-key=%s; expires=%s; path=/' % (session_key, exp_date)

if __name__ == '__main__':
    pass