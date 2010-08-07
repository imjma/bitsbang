#!/usr/bin/env python

from functools import wraps

def is_login(method):
    @wraps(method)
    def self_login(self, *args, **kwargs):
        if not self.user is None:
            return method(self,*args,**kwargs)
        return self.redirect('/signin')
    return self_login

if __name__ == '__main__':
    pass