#!/usr/bin/env python

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from django.http import parse_cookie

from models import Setting
from bitsable.bitsbang.user.models import Session

class PublicHandler(webapp.RequestHandler):
    """Public Handler"""
    def initialize(self, request, response):
        """initial webapp.RequestHandler"""
        webapp.RequestHandler.initialize(self, request, response)
        self.setting = Setting.get_setting()
        self.template_value = {'setting' : self.setting}
        
        # check cookies and find user
        cookies = parse_cookie(self.request.headers.get("Cookie", ""))
        self.session_key = cookies.get('bitsable-session-key', None)
        
        self.user = None
        if self.session_key is not None and len(self.session_key) == 40:
            logging.info("session_key:%s" % self.session_key)
            self.user = Session.get_user_by_session(self.session_key)
        self.template_value['user'] = self.user

    def render(self, template_file):
        """render template file"""
        template_file = 'themes/default/%s' % template_file
        path = os.path.join(os.path.dirname(__file__), r'../../', template_file)
        self.response.out.write(template.render(path, self.template_value))
        
    def error(self, error):
        pass

if __name__ == '__main__':
    pass
