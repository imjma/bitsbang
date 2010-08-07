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

if __name__ == '__main__':
    pass