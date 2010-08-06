#!/usr/bin/env python

from google.appengine.ext import db

class Setting(db.Model):
    title = db.StringProperty(default='Bitsbang')

    @classmethod
    def get_setting(self):
        """get setting value"""
        setting = self.get_by_key_name('default')
        if setting is None:
            setting = Setting(key_name='default')
            setting.title = 'Bitsbang'
            setting.put()
        return setting

if __name__ == '__main__':
    pass
