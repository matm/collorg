#!/usr/bin/env python
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

import os
import collorg
import datetime
from functools import wraps
from collorg.utils import db_connector
from collorg.orm.db import Db
from collorg.orm.table import Table

def _template(func):
    @wraps(func)
    def wrapper(self, **kwargs):
        # kwargs: cog_write, cog_moderate, cog_admin
        kw = kwargs
        begin = datetime.datetime.now()
        ctrl = self._cog_controller
        cog_user = ctrl.user
        if 'no_cog_user' in kwargs:
            cog_user = None
        cog_charset = ctrl._charset
        cog_environment = ctrl.cog_exec_env
        func_name = func.func_name
#        cog_environment = None
        cog_reminder = kw.pop('cog_reminder', "")
        res = []
        if 'cog_first_call' in kwargs.keys() and self._is_of_type_post:
            if not ctrl.check_visibility(self):
                return self.w3access_denied()
        kw.pop('cog_first_call', None)
        #? wma
        if not ctrl.check(self, func):
            return "<!-- access denied -->"
        if 'cog_alt_target' in kw:
            kw['target'] = kw['cog_alt_target']
        f_res = func(
            self, cog_charset=cog_charset, cog_user=cog_user,
            cog_environment=cog_environment, **kw)
        begin_funct = datetime.datetime.now()
        if ctrl.cog_trace:
            res.append("<!-- begin %s.%s (prep: %ss) -->" % (
                self.__class__.__name__, func_name, begin_funct - begin))
        res.append(f_res.strip())
        duration = datetime.datetime.now() - begin_funct
        if ctrl.cog_trace:
            res.append("<!-- end %s.%s (duration: %ss)-->" % (
                self.__class__.__name__, func_name, duration))
        res.append(cog_reminder.encode(ctrl._charset))
        return "\n".join(res)
    return wrapper

class Controller(object):
    _anonymous = None
    _visitor = None
    _cog_aa_tasks = None
    _cog_ca_tasks = None
    _charset = None
    _debug = False
    __anonymous_role = None
    __visitor_role = None
    __d_anonymous_access = {}
    __d_visitor_access = {}
    __d_ca_access = {}
    __d_inh_tree = {}
    __d_accessible_actions = {}
    _d_actions = {}
    _d_actions_by_oid = {}
    _d_check = {}
    __app_path = None
    def __init__(self, config_file = None):
        self._kwargs = {}
        #DEBUG TEMPLATE IN CONSOLE self.user = None
        self._cog_ajax = None
        self._cog_method = None
        self._cog_ref_oid = None
        self._cog_fqtn_ = None
        self._cog_oid_ = None
        self._cog_cmd = None
        self.cog_trace = False
        self.__session = None
        self._session_key = None
        self._json_res = {}
        self.__collorg_path = os.path.dirname(collorg.__file__)
        self.__repos_path = None
        self.__db_name = config_file
        if self.__db_name is None:
            self.__repos_path, self.__db_name = db_connector.get_cog_infos()
        if self.__repos_path is None and self.__db_name == 'collorg_db':
            self.__repos_path = self.__collorg_path
        self.db = Db(self, *db_connector.ini_connect(self.__db_name))
        if 'charset' in self.db._cog_params:
            self._charset = self.db._cog_params['charset']
        self.__debug = False
        if 'debug' in self.db._cog_params:
            Controller._debug = self.db._cog_params['debug']
            open("/tmp/cog_sql", "w")
            try:
                os.chmod("/tmp/cog_sql", "0777")
            except:
                pass
        if not self._d_actions:
            self.__set_app_path()
            self.__get_aa_tasks()
            self.__get_ca_tasks()
            self.__load_actions()
        self.__user_actions = None
        self.d_auth = {}


    def check_visibility(self, obj):
        if obj.cog_oid_.value and not obj.check_visibility(
            cog_user=self.user):
                return False
        return True

    def __set_app_path(self):
        tmp = __import__(
            'collorg_app', globals(), locals(), [], -1)
        Controller.__app_path = "{}/{}".format(
            tmp.__path__[0], self.__db_name)

    @property
    def app_path(self):
        return self.__app_path

    @property
    def collorg_path(self):
        return self.__collorg_path

    def clear(self):
#        open("/tmp/cog_sql", "w")
#        open("/tmp/cog_trace", "w")
        self._kwargs = {}
        self._cog_ajax = None
        self._cog_method = None
        self._cog_fqtn_ = None
        self._cog_oid_ = None
        self._cog_cmd = None
        self.__user_actions = None
        self.db.rollback()
        self.db.new_cursor()

    def __load_actions(self):
        actions = self.db.table('collorg.application.action')
        for action in actions:
            self._d_actions[(
                action.name_.value, action.data_type_.value)] = action
            self._d_actions_by_oid[action.cog_oid_.value] = action
        check = self.db.table('collorg.application.check')
        check.cog_light = True
        for elt in check:
            if not elt.requires_ in self._d_check:
                self._d_check[elt.requires_] = []
            self._d_check[elt.requires_].append(elt.required_)

    def get_action(self, obj, method_name):
        fqtn = obj.fqtn
        if not (method_name, obj.fqtn) in self._d_actions:
            for pfqtn in obj.parents_fqtns():
                if (method_name, pfqtn) in self._d_actions:
                    fqtn = pfqtn
                    break
        if not (method_name, fqtn) in self._d_actions:
            raise RuntimeError("{} {} not found\n{}\n".format(
                fqtn, method_name, self._d_actions))
            return None
        return self._d_actions[(method_name, fqtn)]

    def check_action(self, obj, method):
        """
        """
        if (obj.fqtn, method) in self.__d_accessible_actions:
            return True
        action = self.db.table('collorg.application.action')
        action.name_.set_intention(method)
        action.data_type_.set_intention(obj.fqtn)
        for in_obj in self._cog_inherits(obj):
            action.data_type_ += (in_obj.fqtn, '=')
        try:
            assert action.exists()
        except:
            raise RuntimeError("{}.{} not accessible<br>{}".format(
                obj.fqtn, method, action.select(just_return_sql = True)))
        self.__d_accessible_actions[(obj.fqtn, method)] = True

    @property
    def _d_anonymous_access(self):
        return self.__d_anonymous_access

    @property
    def _d_visitor_access(self):
        return self.__d_visitor_access

    @property
    def _session(self):
        return self.__session

    @property
    def db_name(self):
        return self.__db_name

    @property
    def app_module(self):
        db_name = self.db_name
        if db_name == "collorg_db":
            return "collorg"
        return "collorg_app.{}".format(db_name)

    @property
    def repos_path(self):
        return self.__repos_path

    def process(self):
        raise NotImplementedError

    def __get_aa_tasks(self):
        """
        Loads the anonymous and authenticated tasks once for all.
        """
        if Controller._cog_aa_tasks is not None:
            return
        view = self.db.table('collorg.access.view.access_aa')
        view.cog_light = True
        view.goal_name_.set_intention("Anonymous navigation")
        view.goal_name_ += ("Authenticated navigation", "=")
        #view.in_menu_.set_intention(True)
        view._cog_order_by = [view.task_name_]
        Controller._cog_aa_tasks = view.select().dict_by(
            view.fqtn_, view.goal_name_)
        for key, val in Controller._cog_aa_tasks.items():
            if key[1] == 'Anonymous navigation':
                Controller.__d_anonymous_access[key] = [
                    elt.name_ for elt in val]
            if key[1] == 'Authenticated navigation':
                Controller.__d_visitor_access[key] = [
                    elt.name_ for elt in val]

    def __get_ca_tasks(self):
        """
        Loads the "Collorg actor" tasks once for all.
        """
        if Controller._cog_ca_tasks is not None:
            return
        view = self.db.table('collorg.access.view.access_ca')
        view.cog_light = True
        view._cog_order_by = [view.task_name_]
        Controller._cog_ca_tasks = view.select().dict_by(view.fqtn_)
        for key, val in Controller._cog_ca_tasks.items():
            ca_val = [elt.name_ for elt in val]
            Controller.__d_ca_access[key[0]] = ca_val

    def __check(self, session_key, l_data_oid, obj, action):
        method_name = action.name_.value
        av = self.db.table('collorg.access.view.access')
        av.cog_light = True
        for data_oid in l_data_oid:
            av.data_oid_ += (data_oid, '=')
        av.name_.set_intention(method_name)
        av.session_key_.set_intention(session_key)
        return av.exists()

    def _cog_inherits(self, obj):
        # pb with table._cog_inherits
        if obj.fqtn in self.__d_inh_tree:
            return self.__d_inh_tree[obj.fqtn]
        inh_tree = []
        for elt in type.mro(type(obj)):
            if elt is Table:
                break
            inh_tree.append(elt(obj.db))
        self.__d_inh_tree[obj.fqtn] = inh_tree
        return inh_tree

    def check_required(self, action, **kwargs):
        """
        The execution of an action can be constained by the result of
        another action (the check action).
        The constrain is considered ok if the "check action" returns an
        empty string.
        This mecanism is used to display write icons in header only if
        a user has write access to the data.
        """
        action_oid = action.cog_oid_.value
        ok = True
        if action_oid in self._d_check:
            required = self._d_check[action_oid]
            for elt in required:
                check_action = self._d_actions_by_oid[elt]
                res = eval("kwargs['env'].{}(**kwargs)".format(
                    check_action.name_)).strip()
#                open("/tmp/cog_xxx", "a").write("{}: {}\n".format(
#                    check_action.name_, res))
                if not res:
                    ok = False
        return ok

    def __check_da_dv(self, obj, method_name, func, dav):
        for elt in self._cog_inherits(obj):
            akey = (elt.fqtn, func)
            if akey in dav and method_name in dav[akey]:
                return True
        return False

    def __check_ca(self, obj, action):
        """
        The action is granted to the user if and only if there is
        a granted access between obj and the action.
        """
        assert action.write_.value is not None
        method_name = action.name_.value
        oa = self.db.table('collorg.core.oid_table')
        oa.cog_oid_.set_intention(obj.cog_oid_.value)
        dca = Controller.__d_ca_access
        if not self.user.has_access(oa, action.write_.value):
            return False
        for fqtn in obj.parents_fqtns():
            if(fqtn in dca and method_name in dca[fqtn]):
                return True
        return False

    def check(self, obj, func):
        """
        @returns True if access is granted, False otherwise.
        Anonymous and visitors accesses have been loaded once for all
        """
        action = self.get_action(obj, func.func_name)
        method_name = action.name_.value
        if self.__check_da_dv(
            obj, method_name, "Anonymous navigation",
            Controller.__d_anonymous_access):
            return True
        if self.user is None:
            return False
        else:
            if self.__check_da_dv(
                obj, method_name, "Authenticated navigation",
                Controller.__d_visitor_access):
                return True
            elif self.__check_ca(obj, action):
                return True
            else:
                # access is granted
                return self.__check(
                    self._session_key, [obj.cog_oid_.value], obj, action)

    def _unicode(self, str_):
        if type(str_) is not unicode:
            return unicode("%s" % str_, self._charset)
        return str_

    def add_json_res(self, dict_):
        """shouldn't we call this method set_json_res"""
        for key, val in dict_.items():
            self._json_res[key] = self._unicode(val)

    def _get_tasks_menu(self, data_oid):
        av = self.db.table('collorg.access.view.access')
        av.data_oid_.set_intention(data_oid)
        av.session_key_.set_intention(self._session_key)
        av.in_menu_.set_intention(True)
        av._cog_order_by = [av.task_name_]
        return av.select().dict_by(av.fqtn_, av.goal_name_)
