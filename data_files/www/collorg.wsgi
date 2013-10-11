#!python
#-*- coding: utf-8 -*-

from webob import Response
from collorg.controller.web import WebController
from pprint import pformat
import cProfile

alas_output = """<!doctype html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body>
<h5>%s</h5>
<pre>
%s
</pre>
</body>
</html>
"""

db_name = None
controller = None
debug = True

def application(environ, start_response):
    try:
        global db_name
        global controller
        if controller is None:
            db_name = db_name or environ['DOCUMENT_ROOT'].split('/')[-1:][0]
            try:
                controller = WebController(db_name)
            except Exception as err:
                return alas(err, environ, start_response)
                if debug:
                    raise "collorg.wsgi error: {}".format(err)
        if debug:
            pr = cProfile.Profile()
            pr.enable()
        result = controller.process(environ, start_response)
        if debug:
            pr.disable()
            pr.dump_stats("/tmp/cog_profile")
        return result
    except Exception as err:
        controller = None
        return alas(err, environ, start_response)

def alas(err, environ, start_response):
    if not len("%s" % err):
        err = ("Oups! could something went wrong? "
            "Have you got a console at hand?")
    response = Response()
    response.unicode_body = unicode(
        alas_output % (err, pformat(environ)))
    return response(environ, start_response)
