#!/usr/bin/env python

from bitsable.bitsbang.spam.models import Spam
from bitsable.bitsbang.spam.models import SubSpam

def find_spam(self, spamid):
    spam = Spam.get_by_id(int(spamid))
    if spam is None:
        return self.redirect('/')
    return spam

def find_subspam(self, spamid):
    spam = SubSpam.get_by_id(int(spamid))
    if spam is None:
        return self.redirect('/')
    return spam
    
def can_spam(self, spamid):
    spam = Spam.get_by_id(int(spamid))
    if spam is None:
        return self.redirect('/')
    if self.user.key() == spam.user.key():
        return self.redirect('/spam/%s/' % spamid)
    subspam = SubSpam.all().filter('parent_spam = ', spam).filter('user = ', self.user).get()
    if not subspam is None:
        return self.redirect('/spam/%s/' % spamid)
    return spam

if __name__ == '__main__':
    pass