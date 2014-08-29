# -*- coding: utf-8 -*-
'''
    madrid prototype
'''

import os

from google.appengine.ext import ndb

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions = ['jinja2.ext.autoescape'],
        autoescape = True)

class VocabularyNote(ndb.Model):
    name = ndb.StringProperty()

class Vocabulary(ndb.Model):
    eng = ndb.StringProperty()
    kor = ndb.StringProperty()
    again = ndb.BooleanProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello')

class VocabularyUploadHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('pages/upload.html')
        self.response.out.write(page.render())

    def post(self):

        note_name = self.request.get('note_name')
        raw_voca_list = self.request.get('voca_list')

        note_list = VocabularyNote.query(VocabularyNote.name==note_name).fetch()

        # create Vocabulary Note if VocabularyNote named note_name
        if 0 >= len(note_list):
            voca_note = VocabularyNote()
            voca_note.name = note_name
            voca_note.put()

        # insert vocabulary
        for word in raw_voca_list.readlines():

            # assumed each word separated by *
            eng_kor_str = word.split('*')

            voca = Vocabulary(parent=ndb.Key(VocabularyNote, note_name))
            voca.eng = eng_kor_str[0]
            voca.kor = eng_kor_str[1]
            voca.again = False
            voca.put()

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', VocabularyUploadHandler),
], debug=True)

