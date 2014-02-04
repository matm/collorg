#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
the uploader uploads (surprise) a file and attaches it to a data.
A file is only uploaded ounce
"""

import sys
if sys.version >= '3':
    unicode = str
from webob import Response
import cgi
import os
import unicodedata
import json
from collorg.controller.web import WebController

uploader = None

def log(machin):
    open("/tmp/cog_uploader.log", "a+").write(
        "%s\n%s\n" % (str(machin), 70*"-"))

class Uploader(object):
    def __init__(self, conf_file):
        self.db = WebController(conf_file).db
        self.file_name = None
        self.sfile_name = None
        self.user = None
        self.data = None

    def reset(self):
        self.file_name = None
        self.sfile_name = None
        self.user = None
        self.data = None

    #import cgitb; cgitb.enable()
    def __unicode(self, str_):
        if type(str_) is not unicode:
            return unicode("%s" % str_, "utf-8")
        return str_

    def strip_accents(self, str_):
        return unicodedata.normalize(
            'NFKD', str_).encode('ASCII', 'ignore').decode('ASCII')

    def attach_file(self):
        attach = self.db.table('collorg.communication.attachment')
        attach.attach(self.file_, self.data, self.user, self.description)

    def load_file(self, fs):
        __json = {}
        # Generator to buffer file chunks
        def fbuffer(f, chunk_size=10000):
           while True:
              chunk = f.read(chunk_size)
              if not chunk: break
              yield chunk

        # A nested FieldStorage instance holds the file
        fileitem = fs['file']
        session_key = fs['cog_session'].value
        self.user = self.db.table(
            'collorg.web.session', key_ = session_key)._user_.get()
        target = fs['cog_target'].value
        data_oid = fs['cog_oid_'].value
        self.data = self.db.table(
            'collorg.core.base_table', cog_oid_ = data_oid).get()
        self.description = ''
        if 'description_' in fs:
            self.description = fs['description_'].value

        # Test if the file was uploaded
        if fileitem.filename:

           # strip leading path from file name to avoid directory traversal attacks
           self.file_name = unicode(
               os.path.basename(fileitem.filename), encoding='utf-8')
           self.sfile_name = self.strip_accents(self.file_name)
           tmp_file_name = '%s/tmp/%s' % (
               self.db._cog_params['upload_dir'], self.sfile_name)
           tmp_file = open(tmp_file_name, 'wb', 10000)

           # Read the file in chunks
           for chunk in fbuffer(fileitem.file):
              tmp_file.write(chunk)
           tmp_file.close()
           file_ = self.db.table('collorg.communication.file')
           # the file is stored in tmp directory.
           self.file_ = file_.upload(
               self.file_name, self.sfile_name, self.user).get()
           self.attach_file()
           message = 'The file "%s" was attached successfully' % (
               fileitem.filename)

        else:
           message = 'No file was uploaded'
        __json['#%s' % (target)] = {'action':'html', 'content':message}
        return self.__unicode(json.dumps(__json))

def application(environ, start_response):
    fs = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    log(fs)
    global uploader
    if uploader is None:
        uploader = Uploader(fs['db_name'].value)
    uploader.reset()
    response = Response()
    response.unicode_body = uploader.load_file(fs)
    return response(environ, start_response)
