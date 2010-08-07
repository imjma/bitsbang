#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from bitsable.bitsbang.main import PublicHandler
from bitsable.bitsbang.spam.models import Spam
from bitsable.bitsbang.util.security import is_login

class SpamHandler(PublicHandler):
    """spam handler"""
    def get(self, spamid = None):
        if spamid is None:
            spams = Spam.all().filter('parent_spam = ', None).order('-updated_at').fetch(10)
            self.template_value['spams'] = spams
            return self.render('spam/index.html')
        else:
            spam = Spam.get_by_id(int(spamid))
            self.template_value['spam'] = spam
            subspams = Spam.all().filter("parent_spam = ", spam)
            self.template_value['subspams'] = subspams
            if self.user is not None:
                self.template_value['can_spam'] = True
            return self.render('spam/show.html')

class NewSpamHandler(PublicHandler):
    """new spam handler"""
    @is_login
    def get(self, spamid = None):
        self.template_value['this_url'] = '/spam/new'
        if not spamid is None:
            parent_spam = Spam.get_by_id(int(spamid))
            self.template_value['spam'] = parent_spam
            self.template_value['back_url'] = '/spam/%s' % spamid
            self.template_value['this_url'] = '/spam/%s/new' % spamid
        self.render('spam/new.html')
    
    @is_login 
    def post(self, spamid = None):
        self.template_value['this_url'] = '/spam/new'
            
        title = self.request.get('title').strip()
        sub_title = self.request.get('sub_title').strip()
        comment = self.request.get('comment').strip()

        ui_interact = self.request.get('ui_interact').strip()
        gameplay = self.request.get('gameplay').strip()
        replicability = self.request.get('replicability').strip()
        highlight = self.request.get('highlight').strip()
        
        errors = 0
        
        parent_spam = None
        if not spamid is None:
            parent_spam = Spam.get_by_id(int(spamid))
            self.template_value['spam'] = parent_spam
            self.template_value['this_url'] = '/spam/%s/new' % spamid
            title = parent_spam.title
            

        # if len(title) == 0 and spamid is None:
        #     errors += 1
        #     self.template_value['title_error'] = 'can\'t be blank'
        # else:
        #     self.template_value['title_error'] = 'ok'
        #     
        # if len(comment) == 0:
        #     errors += 1
        #     self.template_value['comment_error'] = 'can\'t be blank'
        # else:
        #     self.template_value['comment_error'] = 'ok'
        
        mandatoryList = ['title', 'comment']
        for varname in mandatoryList:
            var = eval(varname)
            self.template_value[varname] = var
            if len(var) == 0:
                errors += 1
                self.template_value[varname + '_error'] = 'can\'t be blank'
            else:
                self.template_value[varname + '_error'] = 'ok'
                
        varList = ['title', 'sub_title', 'comment']
        for varname in varList:
            var = eval(varname)
            self.template_value[varname] = var
        
        ratingList = ['ui_interact', 'gameplay', 'replicability', 'highlight']

        for rating in ratingList:
            var = eval(rating)
            self.template_value[rating] = var
            if var.isdigit():
                self.template_value[rating + '_error'] = 'ok'
            else:
                errors += 1
                self.template_value[rating + '_error'] = 'is empty or not digit'

        if errors > 0:
            return self.render('/spam/new.html')
            
        ui_interact = int(ui_interact)
        gameplay = int(gameplay)
        replicability = int(replicability)
        highlight = int(highlight)

        spam = Spam.new(title, sub_title, comment, self.user, ui_interact, gameplay, replicability, highlight, parent_spam)
        self.redirect('/spam')

class EditSpamHandler(PublicHandler):
    @is_login
    def get(self):
        pass

def main():
    application = webapp.WSGIApplication([('/spam', SpamHandler),
                                            ('/spam/new', NewSpamHandler),
                                            ('/spam/(?P<spamid>[0-9]+)', SpamHandler),
                                            ('/spam/(?P<spamid>[0-9]+)/new', NewSpamHandler),
                                            ('/spam/(?P<spamid>[0-9]+)/edit', EditSpamHandler)],
                                         debug=True)
    util.run_wsgi_app(application)
    
if __name__ == '__main__':
    main()