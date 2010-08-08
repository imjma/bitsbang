#!/usr/bin/env python

import logging

from google.appengine.ext import db

from bitsable.bitsbang.user.models import User

class SpamRating(db.Model):
    """spam rating pool"""
    user = db.ReferenceProperty(User)
    ui_interact = db.RatingProperty(required=True)
    gameplay = db.RatingProperty(required=True)
    replicability = db.RatingProperty(required=True)
    highlight = db.RatingProperty(required=True)
    
class SpamBasic(db.Model):
    sub_title = db.StringProperty()
    comment = db.TextProperty(required=True)
    
    user = db.ReferenceProperty(User, collection_name='user_set')
    rating = db.ReferenceProperty(SpamRating)

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

class Spam(SpamBasic):
    """Spam bal"""
    title = db.StringProperty(required=True, indexed=True)
    last_spam = db.ReferenceProperty(User, collection_name='last_spam_set')
    spam_count = db.IntegerProperty()
    
    average_ui_interact = db.FloatProperty()
    average_gameplay = db.FloatProperty()
    average_replicability = db.FloatProperty()
    average_highlight = db.FloatProperty()
    average_rating = db.FloatProperty()
        
    @classmethod
    def new(self, title, sub_title, comment, user, ui_interact, gameplay, replicability, highlight):
        spam = Spam(title = title, comment = comment)
        spam.sub_title = sub_title
        spam.user = user
        spam.average_ui_interact = float(ui_interact)
        spam.average_gameplay = float(gameplay)
        spam.average_replicability = float(replicability)
        spam.average_highlight = float(highlight)
        spam.average_rating = (spam.average_ui_interact + spam.average_gameplay + spam.average_replicability + spam.average_highlight) / 4
        spam.last_spam = user
        spam.spam_count = 1
        spam.put()
        
        logging.info('new spam - username: %s, spam: %s' % (user.username, spam.key().id()))
        
        # put rating into rating pool
        rating = SpamRating(ui_interact = ui_interact, gameplay = gameplay, replicability = replicability, highlight = highlight)
        rating.user = user
        rating.put()
        
        spam.rating = rating
        spam.put()
        return spam

class SubSpam(SpamBasic):
    parent_spam = db.ReferenceProperty(Spam)
    
    @classmethod
    def new(self, sub_title, comment, user, ui_interact, gameplay, replicability, highlight, parent_spam):
        spam = SubSpam(comment = comment)
        spam.sub_title = sub_title
        spam.user = user
        spam.parent_spam = parent_spam
        spam.put()
        
        logging.info('new sub spam - username: %s, subspam: %s' % (user.username, spam.key().id()))
        
        # put rating into rating pool
        rating = SpamRating(ui_interact = ui_interact, gameplay = gameplay, replicability = replicability, highlight = highlight)
        rating.user = user
        rating.put()
        
        #update parent spam averge rating, count, and spam
        if spam.is_saved() and parent_spam is not None:
            spam_count = parent_spam.spam_count + 1
            parent_spam.last_spam = user
            parent_spam.average_ui_interact = (parent_spam.average_ui_interact * parent_spam.spam_count + ui_interact) / spam_count
            parent_spam.average_gameplay = (parent_spam.average_gameplay * parent_spam.spam_count + gameplay) / spam_count
            parent_spam.average_replicability = (parent_spam.average_replicability * parent_spam.spam_count + replicability) / spam_count
            parent_spam.average_highlight = (parent_spam.average_highlight * parent_spam.spam_count + highlight) / spam_count
            parent_spam.average_rating = (parent_spam.average_ui_interact + parent_spam.average_gameplay + parent_spam.average_replicability + parent_spam.average_highlight) / 4
            parent_spam.spam_count = spam_count
            parent_spam.put()
        
        spam.rating = rating
        spam.put()
        return spam

if __name__ == '__main__':
    pass