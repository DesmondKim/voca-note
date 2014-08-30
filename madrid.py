# -*- coding: utf-8 -*-
'''
    madrid prototype
'''

import os
import urllib
import hashlib

from google.appengine.ext import ndb

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions = ['jinja2.ext.autoescape'],
        autoescape = True)

class VocabularyNote(ndb.Model):
    name = ndb.StringProperty()
    link = ndb.StringProperty()

class Vocabulary(ndb.Model):
    eng = ndb.StringProperty()
    kor = ndb.StringProperty()
    again = ndb.BooleanProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):

        note_list = VocabularyNote.query()
        page_value = {
                'note_list': note_list
        }

        page = JINJA_ENVIRONMENT.get_template('pages/main.html')
        self.response.out.write(page.render(page_value))

class VocabularyUploadHandler(webapp2.RequestHandler):

    def get(self):
        page = JINJA_ENVIRONMENT.get_template('pages/upload.html')
        self.response.out.write(page.render())

    def post(self):

        note_name = self.request.get('note_name')
        raw_voca_list = self.request.get('voca_list')

        note_list = VocabularyNote.query(VocabularyNote.name==note_name).fetch()

        note_link = None

        # create Vocabulary Note if VocabularyNote named note_name
        if 0 >= len(note_list):
            voca_note = VocabularyNote()
            voca_note.name = note_name
            voca_note.link = hashlib.sha512(u' '.join([note_name, ' ']).encode('utf-8')).hexdigest()[0:16]
            voca_note.put()

            note_link = voca_note.link

        # insert vocabulary
        for word in raw_voca_list.encode('utf-8').split('\n'):

            # assumed each word separated by *
            eng_kor_str = word.split('*')

            if note_link and 1 < len(eng_kor_str):
                voca = Vocabulary(parent=ndb.Key(VocabularyNote, note_link))
                voca.eng = eng_kor_str[0]
                voca.kor = eng_kor_str[1]
                voca.again = False
                voca.put()

        self.redirect('/')

class VocabularyNoteHandler(webapp2.RequestHandler):
    def get(self, note_link):
        note_link = str(urllib.unquote(note_link))

        voca_list = Vocabulary.query(ancestor=ndb.Key(VocabularyNote, note_link)).fetch()
        self.response.write(voca_list)

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', VocabularyUploadHandler),
    ('/note/([^/]+)?', VocabularyNoteHandler),
], debug=True)

