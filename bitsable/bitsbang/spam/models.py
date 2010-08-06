#!/usr/bin/env python

from google.appengine.ext import db

from bitsable.bitsbang.user.models import User

class Spam(db.Model):
    """Spam by bal"""
    title = db.StringProperty(required=True, indexed=True)
    sub_title = db.StringProperty()
    body = db.TextProperty(required=True)
    
    user = db.ReferenceProperty(User)
    
    parent_spam = db.SelfReferenceProperty()
    spam_num = db.IntegerProperty()
    rating_ui_interact = db.RatingProperty()
    rating_gameplay = db.RatingProperty()
    rating_replicability = db.RatingProperty()
    rating_highlight = db.RatingProperty()

if __name__ == '__main__':
    pass