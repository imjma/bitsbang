#!/usr/bin/env python

import logging

from google.appengine.ext import db

from bitsable.bitsbang.util.base import *

class User(db.Model):
    username = db.StringProperty(required=True, indexed=True)
    email = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)
    
    username_lower = db.StringProperty(indexed=True)
    
    activation_key = db.StringProperty(indexed=True)
    
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    
    def put(self):
        """save lower username / email"""
        self.username_lower = self.username.lower()
        self.email = self.email.lower()
        super(User, self).put()
        
    @classmethod
    def new(self, username, email, password):
        user = self(username = username, email = email, password = password)
        user.auth_key = encrypt(random_str(6) + ':' + password)
        user.put()
        if user.is_saved():
            session = Session.new(user, 30)
            return user,session
        else:
            return None,None
        
    @classmethod
    def login(self, username, password):
        user = self.all().filter('username_lower = ', username.lower).get()
        if user is None:
            return None,None
        logging.info('login - username: %s, password: %s' % (username, password))
        if user.password == encrypt(password):
            session = Session.new(user, 30)
            return user,session
        return None,None
        
class Session(db.Model):
    user = db.ReferenceProperty(User)
    exp_date = db.DateTimeProperty()
    
    @classmethod
    def new(self, user, exp_date=30):
        session_key = encrypt('%s:%s' % (random_str(6), user.password))
        logging.info("%s:session_key:%s" % (user.username, session_key))
        exp_date = datetime.datetime.now() + datetime.timedelta(days=exp_date)
        session = Session(key_name = session_key, user = user, exp_date = exp_date)
        session.put()
        return session
        
    @classmethod
    def get_user_by_session(self, session_key):
        session = self.get_by_key_name(session_key)
        return None if session is None else session.user
        

if __name__ == '__main__':
    pass