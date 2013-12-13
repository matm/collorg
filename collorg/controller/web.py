#-*- coding: utf-8 -*-

### Copyright © 2011 Joël Maïzi <joel.maizi@lirmm.fr>
### This file is part of collorg

### collorg is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
if sys.version >= '3':
    unicode = str
from .controller import Controller
from collorg.utils.cache.client import Client

from Cookie import SimpleCookie
#from BeautifulSoup import BeautifulSoup
from webob import Request, Response, html_escape
from webob.acceptparse import Accept

import json
from pprint import pformat
import datetime
import uuid
import md5
import re
import traceback
import gettext

raise_error = False

class WebController(Controller):
    """
    Web controller.
    """
    __static_body = None
    __topics = {} # topics are loaded on demand
    __site = None
    _d_topics = {} # all topics are loaded once!
    __main_topic = None
    def __init__(self, config_file):
        self.__lang = None
        self.i18n = None
        self.direct_obj_ref = None
        self.cog_exec_env = None
        self.__env_set = False
        self.__nsession = False
        self._begin = None
        self.__cog_target = None
        self._cog_raw = None
        self._cog_ajax = None
        self._script_name = None
        self._server_name = None
        self._url_scheme = None
        self._environ = None
        self.__request = None
        self._session_key = None
        self.__session = None
        self._user = None
        self.__cog_environment = None
        self.__get_request = None
        self.cog_ref_obj = {}
        Controller.__init__(self, config_file)
        self.cache = Client(self)
        self.cache.check()

    def clear(self):
        self.direct_obj_ref = None
        self.cog_exec_env = None
        self.__env_set = False
        self.__nsession = False
        self.__cog_target = None
        self._cog_raw = None
        self._cog_ajax = None
        self._environ = None
        self._user = None
        self.__request = None
        self._session_key = None
        self.__session = None
        self.__get_request = None
        self._json_res = {}
        self.cog_ref_obj = {}
        Controller.clear(self)

    @property
    def env_set(self):
        return self.__env_set

    def __rt(self, template_name):
        """
        reads the templates and returns it's content
        """
        params = self.db._cog_params
        tp = params['templates_path']
        return open("%s/%s.html"%(tp, template_name)).read()

    def __get_tags(self):
        return self.db.table('collorg.communication.tag').search_links()

    def __get_important_posts(self):
        return self.db.table(
            'collorg.communication.blog.view.by_post').important()

    @property
    def new_session(self):
        self.__nsession = True
        self._session_key = uuid.uuid4()
        return self._session_key

    def __get_static_body(self):
        self.db.table('collorg.core.base_table')
        dt = {} # templates dictionary
        params = self.db._cog_params
        html = self.__rt("html")
        dt['head'] = self.__rt("head")
        dt['title'] = self.db.name
        dt['style'] = self.__rt("style")
        dt['javascript'] = self.__rt("javascript")
        dt['head'] = dt['head'] % (
            self._charset, dt['style'], params['icon'], dt['title'],
            dt['javascript'])
        dt['ariadne'] = self.__rt("ariadne")
        dt['top_search'] = self.__rt("top_search")
        dt['body'] = self.__rt("body")
        dt['header'] = self.__rt("header")
        dt['homepage_link'] = self.__rt("homepage_link")
        dt['homepage_link'] = "" #dt['homepage_link'] % (self._script_name)
        dt['search'] = self.__rt("search")
        dt['login_zone'] = self.__rt("login_zone")
        dt['header'] %= (
            dt['homepage_link'], dt['login_zone'])
        dt['login_container'] = self.__rt("login_container")
        dt['body_content'] = self.__rt("body_content")
        dt['footer'] = self.__rt("footer")
        dt['collorg_link'] = self.__rt("collorg_link")
        dt['footer'] %= (dt['collorg_link'])
        dt['body'] %= (
            dt['ariadne'],
            dt['top_search'],
            dt['header'], dt['login_container'],
            dt['body_content'],
            dt['footer'])
        dt['debug'] = self.__rt("debug")
        dt['collorg_link'] = self.__rt("collorg_link")
        html %= (dt['head'].decode(self._charset),
                 dt['body'].decode(self._charset))
        return html

    def __pfce(self, obj):
        return html_escape(str(pformat(obj)))

    def __oid_req(self, **kwargs):
        """
        The controller received a cog_oid. The object representing one
        and only one elt of the table is instanciated.

        @returns: the method cog_method applied to this object.
        @called by: self.__exec
        """
        if not '_cog_fqtn_' in self.__dict__ or not self._cog_fqtn_:
            obj = self.db.get_elt_by_oid(self._cog_oid_)
        else:
            obj = self.db.table(self._cog_fqtn_)
            obj.cog_oid_.set_intention(self._cog_oid_)
            obj.get()
        self.check_action(obj, self._cog_method)
        self.cog_exec_env = obj.get_environment()
        if (self._user is None and obj._is_cog_post and
            obj.visibility_.value == 'public' and
            self._cog_method == 'w3display'):
                cache = obj._cog_get_cache('w3display')
                if cache is not None:
                    return cache
        return eval("obj.{}(**kwargs)".format(self._cog_method))

    def __fqtn_req(self, **kwargs):
        """
        No cog_oid received by the controller but a cog_fqtn.

        @returns: the method referenced by cog_method applied to the object
        instantiated without intention (aka the whole table).
        @called by: self.__exec
        """
        obj = self.db.table(self._cog_fqtn_)
        self.check_action(obj, self._cog_method)
        return eval("obj.{}(**kwargs)".format(self._cog_method))

    def load_site(self):
        #XXX REFACTOR
        path_info = self._path_info
        if self.direct_obj_ref:
            path_info = '/'
        url = "{}{}".format(
            self._environ['HTTP_HOST'], self._environ.get('SCRIPT_NAME', ''))
        site = self.db.table("collorg.web.site")
        if not (url, path_info) in self.__topics:
            topic, w3display_topic  = site.load_topic(
                url, path_info)
            if self.__site is None:
                self.__site = site.get()
            self.__topics[(url, path_info)] = (w3display_topic, topic)
###        self._d_topics = self.__site.load_topics()
        topic = self.__topics[(url, path_info)][1]
        self._cog_cmd = self.__topics[(url, path_info)][0]
        return topic

    @property
    def site(self):
        return self.__site

    @property
    def main_topic(self):
        # Post._w3get_recipient
        if not self.__main_topic:
            self.__main_topic = self.__site.load_topic()[0]
        return self.__main_topic

    @property
    def _session(self):
        return self._session_key

    @property
    def user(self):
        return self._user

    @property
    def cog_environment(self):
        return self.__cog_environment

    def __dumps_json_res(self):
        res = {}
        for key, val in self._json_res.items():
            res[key] = {'content':val, 'action':'html'}
        return json.dumps(res)

    def __get_query_params(self):
        qs = {}
        for query in self.__request.POST, self.__request.GET:
            for key, val in query.items():
                key = key.encode(self._charset)
                val = val.encode(self._charset)
                if key[-2:] == '[]':
                    key = key[:-2]
                    if key not in qs:
                        qs[key] = []
                    qs[key].append(val)
                else:
                    qs[key] = val
        return qs

    def set_ref_obj_oid(self, obj_oid, ref_obj_oid):
        if obj_oid:
            self.cache.set_(
                "ref_obj_oid", self._session_key, (obj_oid, ref_obj_oid))

    def set_env(self, env):
        if not self._session_key:
            return
        self.__env_set = True
        if self.__nsession:
            self.cache.set_("user", self._session_key, None)
            self.cache.set_(
                "creat_date", self._session_key, self._begin)
        self.cache.set_(
            "last_access_date", self._session_key, self._begin)

    def __get_env(self):
        if self._session_key:
            self.cache.get_("last_access_date", self._session_key)
            self.cache.set_(
                "last_access_date", self._session_key, self._begin)
            self.get_user()

    def get_user(self):
        if self._session_key:
            user_oid = self.cache.get_("user", self._session_key)
            if user_oid:
                self._user = self.db.table(
                    'collorg.actor.user', cog_oid_ = user_oid).get()
            else:
                self.delete_cookie('cog_session')

    def set_user(self, user_oid = None):
        self.cache.set_("user", self._session_key, user_oid)

    def del_user(self, key):
        self.cache.del_("user", key)

    def __get_params(self):
        self._kwargs = self.__get_query_params()
        self._cog_ajax = self._kwargs.get('cog_ajax')
        self.__cog_target = self._kwargs.get('cog_target')
        self._cog_raw = self._kwargs.get('cog_raw', None)
        self._cog_method = self._kwargs.get('cog_method', None)
        # cog_method must not contain non-word caracters
        assert self._cog_method is None or \
            re.search('\W', self._cog_method) is None
        if self._cog_method is not None and self._cog_method[0] == '_':
            # we never should receive a protected method...
            self._cog_method = "w3error"
            self._kwargs['cog_method'] = "w3error"
            self._kwargs['cog_error'] = "Can't call a protected method!"
        self._cog_ref_oid = self._kwargs.get('cog_ref_oid', None)
        self._cog_oid_ = self._kwargs.get('cog_oid_', None)
        self._session_key = None
        if 'HTTP_COOKIE' in self._environ:
            cookie_string = self._environ.get('HTTP_COOKIE')
            cookie = SimpleCookie()
            cookie.load(cookie_string)
            if cookie.has_key('cog_session'):
                self._session_key = cookie['cog_session'].value
        self.__cog_environment = self.__get_env()
        self._cog_fqtn_ = self._kwargs.get('cog_fqtn_', None)
        if self._cog_ref_oid and self._cog_ref_oid == self._cog_oid_:
            self._cog_oid_ = None
        self._kwargs['cog_controller'] = self
        self._kwargs['cog_first_call'] = True

    def __reset(self):
        """
        Some things that are always done first
        """
        self._json_res['#cog_debug_link'] = ''
        self._json_res['#cog_debug'] = ''
        self.__get_params()
        self.db._set_controller(self)
        #self._cog_cmd = self.__environment

    def get_page_ref(self, method = None, oid = None):
        method = method or self._cog_method
        oid = oid or self._cog_oid_
        if oid:
            ref = oid
        else:
            env = self._environ
            if env and 'QUERY_STRING' in env:
                ref = md5.new(env['QUERY_STRING']).hexdigest()
            else:
                ref = self.__site.cog_oid_.value
        page_ref = "{}-{}".format(method, ref)
        return page_ref

    def __exec(self):
        """
        constructs the call to the template.
        the template receives
        depends on the arguments passed.
        Case of ajax:
        * one of the three following arguments is expected
        ** a path (specific wsgi)
        ** an oid
        ** a fqtn
        """
        _ = self.i18n.gettext
        if self._cog_oid_:
            self._cog_cmd = self.__oid_req
        elif self._cog_fqtn_:
            self._cog_cmd = self.__fqtn_req
        elif self._cog_ajax is None and self.direct_obj_ref:
            self._cog_cmd = self.direct_obj_ref
        if self._cog_ajax is None:
            actor = self.db.table('collorg.actor.user')
            result = self.__static_body.format(
                self.__site.w3map_link(),
                _("search"), _("search"),
                _("by tag"), _("by user"),
                actor.w3login_link(),
                _("Drag & drop your links here<br>for future reference").decode(
                    self._charset))
            page = self._cog_cmd(**self._kwargs)
            if self._cog_raw:
                return page
            result %= (
                "", #self._json_res['#cog_top_nav_ariadne']),
                self._unicode(page))
            return result
        # ajax
        try:
            result = self._cog_cmd(**self._kwargs)
            if self._cog_raw:
                return result
            duration = datetime.datetime.now() - self._begin
        except Exception as err:
#            open("/tmp/cog_error_log", "a+").write("{}\n".format(err))
            if self.db._cog_params['debug']:
                link, error = self.debug(err.__str__)
                self._json_res['#cog_debug_link'] = link
                self._json_res['#cog_debug'] = self._unicode(error)
                return self.__dumps_json_res()
            if raise_error:
                raise "Web controller error: {}".format(err)
        self._json_res['#cog_duration'] = "%s" % (duration)
        if self._debug:
            link, debug = self.debug()
            self._json_res['#cog_debug_link'] = link
            self._json_res['#cog_debug'] = self._unicode(debug)
        self._json_res[self.__cog_target] = result
        return self.__dumps_json_res()

    def get_cookie(self, key):
        return self._session_key

    def delete_cookie(self, key):
        self.__response.delete_cookie(key)

    def set_cookie(self, key):
        value = self.new_session
        self.__response.set_cookie(key, bytes(value))
        return value

    def process(self, environ, start_response):
        self._begin = datetime.datetime.now()
        if self._debug:
            open("/tmp/cog_sql", "w")
        try:
            self.clear()
            self._environ = environ
#            open("/tmp/cog_tmp_xxx", "w").write("{}".format(environ))
            self._script_name = self._environ.get('SCRIPT_NAME', '')
            self._server_name = self._environ['HTTP_HOST']
            self._url_scheme = self._environ['wsgi.url_scheme']
            self._url = "{}://{}{}".format(
                self._url_scheme, self._server_name, self._script_name)
            self._path_info = self._environ['PATH_INFO'].lower()
            alnum = "[a-z0-9]{4}"
            oid_pattern = '^/{}{}-{}-{}-{}-{}{}{}$'.format(*(alnum,)*8)
            if re.match(oid_pattern, self._path_info):
                obj = self.db.get_elt_by_oid(self._path_info[1:])
                self.add_json_res({'#page_ref':self.get_page_ref()})
                self.direct_obj_ref = obj.w3display
            self.load_site()
            self.__request = Request(environ)
            self.__lang = Accept(str(self.__request.accept_language))
            self.i18n = gettext.translation(
                'messages', '/usr/share/collorg/locale',
                [self.__lang.best_match(('en', 'fr', 'fr-FR')) or 'en'])
            if WebController.__static_body is None:
                WebController.__tags = self.__get_tags()
                WebController.__static_body = self.__get_static_body()
            self.__response = Response()
            self.__reset()
            if not(self._cog_method is None and
                '#page_ref' in self._json_res.keys()):
                    self.add_json_res({'#page_ref':self.get_page_ref()})
            self.__response.unicode_body = self._unicode(self.__exec())
            if(self.__response.content_type != 'text/html' or
                self.__response.status_int != 200):
                # Not an HTML response, we don't want to
                # do anything to it
                return self.__response(environ, start_response)
            # Make sure the content isn't gzipped:
            self.__response.decode_content()
            return self.__response(environ, start_response)
        except Exception as err:
            if self.db._cog_params['debug']:
                response = Response()
                response.unicode_body = self._unicode(err)
                return response(environ, start_response)
            if raise_error:
                raise err

    def debug(self, error = None):
        output = []
        css_style = 'debug hidden toggle'
        css_error = ''
        if error:
            css_style += ' debug_error'
            css_error = 'debug_error'
        title = error and "Error" or "debug"
        link = ( '<span class="link toggle %s" '
            'to_toggle="#cog_debug">%s</span>' % (css_error, title))
        if error:
            output.append('<h2>Error</h2>')
            output.append('<pre>%s</pre>' % (self.__pfce(error)))
            output.append("<h2>Traceback</h2>")
            output.append("<pre>%s</pre>"%(
                traceback.format_exc()))
        output.append('<h2>Main variables</h2>')
        output.append('<pre>')
        output.append('cog_method = %s\n' % (self._cog_method))
        output.append('cog_fqtn_ = %s\n' % (self._cog_fqtn_))
        output.append('cog_oid_ = %s\n' % (self._cog_oid_))
        output.append('cog_ref_oid = %s\n' % (self._cog_ref_oid))
        output.append('</pre>')
        if error:
            post_error = self.db.table(
                'collorg.application.communication.error')
            try:
                post_error.hit(
                    self._cog_fqtn_, self._cog_method, traceback.format_exc())
            except Exception, err:
                sys.stderr.write("Warning! {}\n".format(err))
#                open("/tmp/cog_error_log", "a+").write("{}\n".format(err))
        output.append('<h2>Query string</h2>')
        output.append('<pre>qs = %s</pre>' % (self.__pfce(self.__get_request)))
        output.append('<h2>Command executed</h2>')
        output.append('<pre>cmd = %s</pre>' %(self.__pfce(self._cog_cmd)))
        output.append('<h2>Environ</h2>')
        output.append('<pre>%s</pre>' % (self.__pfce(self._environ)))
        u_output = [self._unicode(elt) for elt in output]
        return link, "\n".join(u_output)
