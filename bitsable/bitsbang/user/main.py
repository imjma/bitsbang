#!/usr/bin/env python

# from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import re
import logging

from bitsable.bitsbang.main import PublicHandler
from bitsable.bitsbang.user.models import User
from bitsable.bitsbang.util.base import *

MIN_USERNAME_LENGTH = 6
MAX_USERNAME_LENGTH = 20
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 20

class SignupHandler(PublicHandler):
    def get(self):
        self.render('signup.html')
        
    def post(self):
        username = self.request.get('username').strip()
        email = self.request.get('email').strip()
        password = self.request.get('password')
        
        errors = 0

        # verification: username
        username_error_value = [u'ok',
        u'can\'t be blank',
        u'' + str(MIN_USERNAME_LENGTH) +' characters or more',
        u'is too long(maximum is ' + str(MAX_USERNAME_LENGTH) + ' characters)',
        u'only use letters, numbers and \'_\'',
    	u'has alredy been taken']

        username_error = 0
        if len(username) == 0:
            errors += 1
            username_error = 1
        elif len(username) < MIN_USERNAME_LENGTH:
            errors += 1
            username_error = 2
        elif len(username) > MAX_USERNAME_LENGTH:
            errors += 1
            username_error = 3
        elif re.search('^[a-zA-Z0-9\-\_]+$', username):
            user = User.gql("WHERE username_lower = :1", username.lower())
            if user.count() > 0:
                errors += 1
                username_error = 5
        else:
            errors += 1
            username_error = 4

        # verification: email
        email_error_value = [u'ok',
        u'can\'t be blank',
        u'should look like an email address',
        u'has alredy been taken',
        u'should a validation email address']

        email_error = 0
        if len(email) == 0:
            errors += 1
            email_error = 1
        elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            if not mail.is_email_valid(email):
                errors += 1
                email_error = 4
            else:
                u = User.gql("WHERE email = :1", email)
                if u.count() > 0:
                    errors += 1
                    email_error = 3
        else:
            errors += 1
            email_error = 2
        
        # email_error = u'ok'
        # if not mail.invalid_email_reason(email, email_error) is None:
        #     errors += 1

        # verification: password
        password_error_value = [u'ok',
        u'can\'t be blank',
        u'' + str(MIN_PASSWORD_LENGTH) +' characters or more (be tricky!)',
        u'is too long(maximum is ' + str(MAX_PASSWORD_LENGTH) + ' characters)']

        password_error = 0
        if len(password) == 0:
            errors += 1
            password_error = 1
        elif len(password) < MIN_PASSWORD_LENGTH:
            errors += 1
            password_error = 2
        elif len(password) > MAX_PASSWORD_LENGTH:
            errors += 1
            password_error = 3

        notice = u''
        if errors == 0:
            hashed_password = encrypt(password)
            user,session = User.new(username, email, hashed_password)
            if user and session:
                set_cookies(self, session.key().name())
                logging.info('signup - username: %s, password: %s' % (username, password))
                # redirect to home page
                self.redirect('/')
            else:
                logging.info('Error ^ signup - username: %s, password: %s' % (username, password))
                notice = u'some errors on saving data'

        self.template_value = ({
            'errors' : errors,
            'notice' : notice,
            'username_error' : username_error_value[username_error],
            'email_error' : email_error_value[email_error],
            # 'email_error' : email_error,
            'password_error' : password_error_value[password_error],
            'username' : username,
            'email' : email
    	})
        self.render('signup.html')
        
class SigninHandler(PublicHandler):
    def get(self):
        self.render('signin.html')
        
    def post(self):
        username = self.request.get('username').strip()
        password = self.request.get('password')
        if len(username) > 0 and len(password) > 0:
            user,session = User.login(username, password)
            if user and session:
                set_cookies(self, session.key().name())
                logging.info('signup - username: %s, password: %s' % (username, password))
                # redirect to home page
                self.redirect('/')

        error_value = u'wrong username and password combination'
        self.template_value = ({
            'notice' : error_value
        })
        self.render('signin.html')

class SignoutHandler(PublicHandler):
    def get(self):
        self.response.headers['Set-Cookie'] ='bitsable-session-key="";path=/'
        self.redirect('/')        


def main():
    application = webapp.WSGIApplication([('/signup', SignupHandler),
                                            ('/signin', SigninHandler),
                                            ('/signout', SignoutHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()