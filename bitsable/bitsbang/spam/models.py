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

class Spam(db.Model):
    """Spam bal"""
    title = db.StringProperty(required=True, indexed=True)
    sub_title = db.StringProperty()
    comment = db.TextProperty(required=True)
    
    user = db.ReferenceProperty(User, collection_name='user_set')
    last_spam = db.ReferenceProperty(User, collection_name='last_spam_set')
    
    parent_spam = db.SelfReferenceProperty()
    spam_count = db.IntegerProperty()
    
    rating = db.ReferenceProperty(SpamRating)
    
    average_ui_interact = db.FloatProperty()
    average_gameplay = db.FloatProperty()
    average_replicability = db.FloatProperty()
    average_highlight = db.FloatProperty()
    average_rating = db.FloatProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    
    def put(self):
        self.average_rating = round((self.average_ui_interact + self.average_gameplay + self.average_replicability + self.average_highlight) / 4, 1)
        super(Spam, self).put()
        
    @classmethod
    def new(self, title, sub_title, comment, user, ui_interact, gameplay, replicability, highlight, parent_spam = None):
        spam = Spam(title = title, comment = comment)
        spam.sub_title = sub_title
        spam.user = user
        spam.parent_spam = parent_spam
        spam.average_ui_interact = float(ui_interact)
        spam.average_gameplay = float(gameplay)
        spam.average_replicability = float(replicability)
        spam.average_highlight = float(highlight)
        spam.last_spam = user
        spam.spam_count = 1
        spam.put()
        
        logging.info('new spam - username: %s, spam: %s' % (user.username, spam.key().id()))
        
        #update parent spam averge rating, count, and spam
        if spam.is_saved() and parent_spam is not None:
            spam_count = parent_spam.spam_count + 1
            parent_spam.last_spam = user
            parent_spam.average_ui_interact = round((parent_spam.average_ui_interact * parent_spam.spam_count + spam.average_ui_interact) / spam_count, 1)
            parent_spam.average_gameplay = round((parent_spam.average_gameplay * parent_spam.spam_count + spam.average_gameplay) / spam_count, 1)
            parent_spam.average_replicability = round((parent_spam.average_replicability * parent_spam.spam_count + spam.average_replicability) / spam_count, 1)
            parent_spam.average_highlight = round((parent_spam.average_highlight * parent_spam.spam_count + spam.average_highlight) / spam_count, 1)
            parent_spam.spam_count = spam_count
            parent_spam.put()
        
        # put rating into rating pool
        rating = SpamRating(ui_interact = ui_interact, gameplay = gameplay, replicability = replicability, highlight = highlight)
        rating.user = user
        rating.put()
        
        spam.rating = rating
        spam.put()
        return spam

if __name__ == '__main__':
    pass