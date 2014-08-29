# -*- coding: utf-8 -*-
'''
    madrid prototype
'''

import os

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions = ['jinja2.ext.autoescape'],
        autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello')

application = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
