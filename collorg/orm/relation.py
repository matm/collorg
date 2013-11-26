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

import inspect
import uuid

from .field import Field
from .customerror import CustomError
import sys

def trace(debug, arg):
    if debug:
        sys.stderr.write("%s\n" % (arg))

class LObj():
    def __init__(self, d_elt, ctrl, safe = True):
        self._cog_controller = ctrl
        self.fqtn = None
        for key, val in d_elt.items():
            if type(val) is str and safe:
                val = val.replace('>', '&gt;').replace('<', '&lt;')
            if key == 'cog_fqtn_':
                self.fqtn = val
            self.__dict__[key] = val

    def raw(self):
        """returns the dict. Used by cog dump"""
        return self.__dict__

class Relation(object):
    def __init__(self, _db):
        if _db:
            self.db = _db
        self.__sql_req_loaded = False
        self.__sql_req = ""
        self._cog_controller = self.db._cog_controller
        self.cog_distinct = False
        self.__id = "r_%s" % id(self)
        self.__extension = []
        self.__retrieved = False
        self.__deja_vu_src = []
        self.__deja_vu_dst = []
        self.__light = False
        self._list = []
        self._cog_limit = None
        self._cog_offset = None

    @property
    def fqtn(self):
        return '%s.%s' % (self._cog_schemaname, self._cog_tablename)

    @property
    def sql_fqtn(self):
        return '"%s"."%s"' % (self._cog_schemaname, self._cog_tablename)

    sql_fqtn_ref = sql_fqtn

    @property
    def cog_type_name(self):
        cn = self.__class__.__name__
        tna = '_{}__cog_type_name'.format(cn)
        if hasattr(self, tna):
            return getattr(self, tna)
        return self.fqtn

    @property
    def sql_req(self):
        return self.__sql_req

    @property
    def id(self):
        return self.__id

    def __cog_light(self, value):
        """
        sets self.__light result to value (True of False)
        if sets to True, the select tuples are returned as dict. Otherwise
        they are instanciated (slow)
        """
        assert value in (True, False)
        self.__light = value

    cog_light = property(fset=__cog_light)

    def dict_by(self, *fields):
        # self represents the extension
        from collections import OrderedDict
        _dict = OrderedDict()
        field_names = [ field.name for field in fields ]
        for elt in self:
            if not self.__light:
                key = tuple("%s" % elt.__dict__["%s_" % (field_name)].val
                    for field_name in field_names)
                if not key in _dict:
                    _dict[key] = []
                _dict[key].append(elt)
            else:
                key = tuple("%s" % elt.__dict__["%s_" % (field_name)]
                    for field_name in field_names)
                if not key in _dict:
                    _dict[key] = []
                _dict[key].append(elt)
        return _dict

    def order_by(self, *args):
        self._cog_order_by = []
        for elt in args:
            if elt is None:
                continue
            try:
                assert elt.__class__ is Field
                self._cog_order_by.append(elt)
            except Exception as e:
                raise RuntimeError("%s\nwrong elt %s. expected Field\n" % (
                    e, elt.__class__.__name__))
        return self

    def cog_limit(self, limit):
        if limit:
            assert type(limit) == int and limit >= 0
            self._cog_limit = limit

    def cog_offset(self, offset):
        if offset:
            assert type(offset) == int and offset >= 0
            self._cog_offset = offset

    @property
    def _cog_extension(self):
        return self.__extension

    def reset(self):
        """
        clear the extension and intention of the self object.
        All the fields are cleared.
        The extention is set to empty list
        """
        for field in self._cog_fields:
            self.__dict__[field.pyname] = field()
        self.__extension = []

    def _cog_new_select(self, fields=None, count=False):
        """
        TEST CONSTRUCTION REQUETE SELECT. SANS DOUTE PAS ICI!!
        """
        if fields is None:
            fields = self._cog_fields
        else:
            self.cog_distinct = True
        req = ["SELECT"]
        l_fields_names = []
        l_fields = []
        for field in fields:
            l_fields_names.append(field.name)
            if not count:
                l_fields.append("%s.%s" % (field.table.id, field.sql_name_as))
            else:
                l_fields.append("%s.%s" % (field.table.id, field.orig_name))
        assert len(l_fields) > 0
        distinct = ""
        if self.cog_distinct:
            distinct = "DISTINCT"
        what_req = "%s" % (",\n".join(l_fields))
        if count:
            what_req = "count(%s(%s))" % (distinct, what_req)
        else:
            what_req = "%s %s" % (distinct, what_req)
        req.append(what_req)
        req.append("FROM\n%s" % (self._cog_get_from()))
        if self._cog_is_constrained():
            req.append(self._cog_get_where())
        o_req = []
        missing_field = False
        if not count and self._cog_order_by:
            o_req.append("ORDER BY")
            o_req.append(",".join([
                #"%s.%s"%(field.table.id, field.name)
                '"%s" %s' % (field.name, field.descending_order)
                for field in self._cog_order_by
            ]))
            if not field.name in l_fields_names:
                missing_field = True
        if not missing_field:
            req.append("\n".join(o_req))
        if self._cog_limit is not None:
            req.append(" LIMIT {}".format(self._cog_limit))
        if self._cog_offset is not None:
            req.append(" OFFSET {}".format(self._cog_offset))
#        self.__sql_req = req
#        self.__sql_req_loaded = True
        return "\n".join(req)

    def _cog_new_count(self, fields=None):
        return self._cog_new_select(fields=fields,count=True)

    def _cog_new_insert(self):
        """
        """
        cog_oid = None
        req = ""
        from collorg.db.core.base_table import Base_table
        class_hierarchy = inspect.getmro(self.__class__)
        oid_req = ""
        if Base_table in class_hierarchy:
            # we duplicate the information in "collorg.core.oid_table"
            cog_oid = uuid.uuid4()
            cog_fqtn = self.fqtn
            oid_req = ("""INSERT INTO "collorg.core".oid_table VALUES """
                        """('%s', '%s')""" % (cog_oid, cog_fqtn))
            self.cog_oid_.set_intention(cog_oid)
            if ('cog_environment_' in self.__dict__ and
                self.cog_environment_.value is None):
                self.cog_environment_.set_intention(cog_oid)
        req += "INSERT INTO\n"
        req += "%s\n" % (self.sql_fqtn)
        l_fields = []
        for field in self._cog_fields:
            if field.is_constrained:
                l_fields.append(field)
        req += "(%s)\n" % ",\n".join(
            [ '"%s"' % field.orig_name for field in l_fields ])
        req += "VALUES\n"
        req += "(%s)" % ",\n".join(
            [ field.quoted_val for field in l_fields ])
        if oid_req:
            req = "BEGIN\n;%s; --++++\n%s;--+++++\nEND;\n" % (req, oid_req)
        return req, cog_oid
        
    def _cog_get_where(self):
        req = []
        req.append("%s" % (self._cog_get_where_inner()))
        for elt in self._list:
            req = ["(%s) %s (%s)" % (
                "\n".join(req), elt[0], elt[1]._cog_get_where_inner(self.id))]
        req.insert(0, "WHERE")
        req = "\n".join(req)
        if req.strip() == "WHERE":
            return ""
        return req

    def _cog_get_where_inner(self, rel_id=None):
        """
        @return: SQL form of where condition
        """
        def _just_cog_oid(self):
            for field in self._cog_fields:
                if field.name == 'cog_oid' and field.value:
                    return field
        l_where = []
        cog_oid = _just_cog_oid(self)
        if cog_oid:
            l_where.append(cog_oid._sql_where_repr(rel_id))
        for field in self._cog_fields:
            ok = True
            if cog_oid:
                ok = field.name != 'cog_oid' and (
                    field.comp != '=' or field.name == 'cog_fqtn')
                if (field.name == 'cog_fqtn' and
                    field.value == 'collorg.core.oid_table'):
                        ok = False
            if ok:
                sql_where_repr = field._sql_where_repr(rel_id)
                if sql_where_repr:
                    l_where.append(sql_where_repr)
        return  " AND\n".join(l_where)

    def _cog_is_constrained(self):
        """
        @return: True if at least one of the fields of self is constrain,
        False otherwise.
        """
        for field in self._cog_fields:
            if field.is_constrained:
                return True
        return False

    def get_extent(
        self, expected = -1, fields = None, just_return_sql = False):
        if not self.__sql_req_loaded:
            sql_req = self._cog_new_select(fields = fields)
        else:
            sql_req = self.sql_req
#        open("/tmp/lag", "a+").write("-->>>\n%s\n---<<<\n" % sql_req)
        if just_return_sql:
            return sql_req
        try:
            extension = self.db.get_query_res(sql_req)
        except Exception as e:
            self.db.rollback()
            raise CustomError("select error: %s\n%s" % (e, sql_req))
        if expected != -1:
            try:
                assert len(extension) == expected
            except:
                raise CustomError("expected %s, got %s tuples\n%s" % (
                        expected, len(extension), sql_req))
        self.__extension = extension
        self.__retrieved = True
        return self

    select = get_extent

    def get(
        self, fields = None, just_return_sql = False, recurse = True,
        reload_ = False):
        if reload_:
            assert self.cog_oid_.value is not None
            for field in self._cog_fields:
                if field.name != 'cog_oid':
                    self.__dict__[field.pyname].set_intention(None)
        #!! offset ?
        res = self.select(
            expected = 1, fields = fields, just_return_sql = just_return_sql)
        if just_return_sql:
            return res
        for key, val in self.__extension[0].items():
            self.__dict__["%s_" % (key)].set_intention(val)
        self.__retrieved = True
        self.__uniq = True
        if 'cog_fqtn_' in self.__dict__ and self.fqtn != self.cog_fqtn_.value:
            obj = self.db.table(self.cog_fqtn_.value)
            obj.cog_oid_.set_intention(self.cog_oid_.value)
            return obj.get()
        return self[0]

    def _cog_count(self, orig, fields, just_return_sql):
        """
        retourne le nombre d'éléments dans la base de donnée correspondant
        à l'intention posée
        """
        #
        sql_req = self._cog_new_count(fields)
        if just_return_sql:
            return sql_req
        try:
            return self.db.get_query_res(sql_req, nodelay = True)[0][0]
        except Exception as e:
            self.db.rollback()
            raise CustomError("Count error: %s\n%s" % (e, sql_req))

    def count(self, fields = None, just_return_sql = False):
        return self._cog_count(
            orig = self, fields = fields, just_return_sql = just_return_sql)

    def exists(self):
        auto_commit = self.db.get_auto_commit()
        self.db.set_auto_commit(True)
        sql = self.select(just_return_sql = True)
        sql += "\nLIMIT 1"
        exists = self.db.fetchone(sql) and True or False
        self.db.set_auto_commit(auto_commit)
        return exists

    def __min_max(self, min_max, field):
        req = []
        req.append('select {}(array["{}"])'.format(min_max, field.name))
        req.append('from {}'.format(self._cog_get_from()))
        req.append(self._cog_get_where())
        sql_req = "\n".join(req)
        res = self.db.get_query_res(sql_req)[0][0][0]
        return res

    def min(self, field):
        return self.__min_max('min', field)

    def max(self, field):
        return self.__min_max('max', field)

    def increment(self, field, value = 1):
        assert float(value)
        req = []
        req.append('update {} set "{}" = "{}" + {}'.format(
            self._cog_get_from(), field.name, field.name, value))
        req.append(self._cog_get_where())
        sql_req = "\n".join(req)
        self.db.raw_sql(sql_req)
        return self
        
#    def __len__(self):
#        return self.count()

    def __iter__(self):
        if len(self.__extension) == 0:
            self.select()
        for elt in self.__extension:
#            if 'cog_ref_obj' in self.__class__.__dict__:
#                oid = elt['cog_oid']
#                for ref_obj in self.cog_ref_obj():
#                    if ref_obj.count() == 1:
#                        ref_oid = ref_obj.get().cog_oid_.value
#                        self._cog_controller.set_ref_obj_oid(oid, ref_oid)
            d_elt = {}
            for key, val in elt.items():
                d_elt["%s_" % (key)] = val
            if self.__light:
                yield(LObj(d_elt, self._cog_controller))
            else:
                res = self.__class__(self.db, **d_elt)
                res.__retrieved = True
                res.__uniq = True
                yield(res)

    def __getitem__(self, idx):
        d_elt = {}
        for key, val in self.__extension[idx].items():
            d_elt["%s_" % (key)] = val
        if self.__light:
            return LObj(d_elt, self._cog_controller)
        return self.__class__(self.db, **d_elt)

    def _cog_get_from(self, debug = False):
        return "%s %s" % (self.sql_fqtn, self.id)

    @property
    def cog_label_fields(self):
        if '_cog_label' in self.__class__.__dict__:
            return self._cog_label[1:]
        else:
            l_fields = []
            for field in self._cog_fields:
                if( field.name != 'cog_oid' and field.pkey and
                    field.sql_type != 'c_oid' ):
                    l_fields.append(field)
            return l_fields

    def cog_label(self):
        if '_cog_label' in self.__class__.__dict__:
            label = self._cog_label[0].format(*self.cog_label_fields)
        else:
            label = ' '.join([field.value for field in self.cog_label_fields])
        return label.strip()

    def __add__(self, other):
        self._list.append(("OR", other))
        return self

    __iadd__ = __add__

    def __mul__(self, other):
        self._list.append(("AND", other))
        return self

    __imul__ = __mul__

    def __sub__(self, other):
        self._list.append(("AND NOT", other))
        return self

    __isub__ = __sub__

    @staticmethod
    def __inherited_fqtns(cls):
        """
        returns the classes inherited by self up to Table
        """
        if not hasattr(cls, '__inherited_classes'):
            cls.__inherited_classes = []
            for base in cls.__bases__:
                if '_cog_schemaname' in base.__dict__:
                    fqtn = "{}.{}".format(
                        base._cog_schemaname, base._cog_tablename)
                    if not fqtn in cls.__inherited_classes:
                        cls.__inherited_classes.append(fqtn)
                    for cfqtn in cls.__inherited_fqtns(base):
                        if not cfqtn in cls.__inherited_classes:
                            cls.__inherited_classes.append(cfqtn)
            cls.__inherited_classes.insert(
                0, "{}.{}".format(cls._cog_schemaname, cls._cog_tablename))
        return cls.__inherited_classes

    def parents_fqtns(self):
        return self.__inherited_fqtns(self.__class__)

    def children_fqtns(self):
        return self.db.metadata.children_fqtns(
            self._cog_schemaname, self._cog_tablename)

    def cog_restrict_to_type(self, fqtn):
        obj = self.db.table(fqtn)
        self.cog_fqtn_ += (fqtn, '=')
        for fqtn in obj.children_fqtns():
            self.cog_fqtn_ += (fqtn, '=')

    def cog_path(self, data_type):
        return None

    def set_class_variable(self, fqtn, *args):
        cvn = "_cv_{}".format(inspect.stack()[1][3])
        cls = self.__class__
        if not hasattr(cls, cvn):
            setattr(cls, cvn, self.db.table(fqtn))
        obj = getattr(cls, cvn)
        for field_name, self_field_name in args:
            obj.__dict__[field_name].set_intention(
                self.__dict__[self_field_name])
        return getattr(self, cvn)
