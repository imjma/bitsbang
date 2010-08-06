#!/usr/bin/env python

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class PublicHandler(webapp.RequestHandler):
	"""Public Handler"""
	def initialize(self, request, response):
		"""initial webapp.RequestHandler"""
		webapp.RequestHandler.initialize(self, request, response)
		self.template_value = {}
		
	def render(self, template_file):
		"""render template file"""
		template_file = 'themes/default/%s' % (template_file)
		path = os.path.join(os.path.dirname(__file__), r'../../', template_file)
		self.response.out.write(template.render(path, self.template_value))
		
if __name__ == '__main__':
	pass