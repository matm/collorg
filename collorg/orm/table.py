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
import os
from datetime import datetime
import time

#from collorg.utils.deco import benchmark, logging, counter
from .relation import Relation
from .field import Field
from .customerror import CustomError

class Table(Relation):
    _cog_base_table = False
    def __load_fields(self):
#        open("/tmp/cog_xxx", "a").write("load {}\n".format(self.fqtn))
        l_fields = self.db.metadata.fields_names(
            self._cog_schemaname, self._cog_tablename)
        for fieldname in l_fields:
            attr_fieldname = "%s_" % (fieldname)
            if not fieldname in self.__dict__:
                attr_fieldname = "%s_" % (fieldname)
                setattr(self,
                         attr_fieldname,
                         Field(self, fieldname))
                self.__l_fields.append(attr_fieldname)
                if self.__dict__[attr_fieldname].pkey:
                    self.__pkey_fields.append(
                        self.__dict__[attr_fieldname].pkey)
        self.__fields_loaded = True

    def __import_templates(self):
        """
        Imports the templates (see <fqtn>/cog/templates) as methods of
        the class.
        Collorg templates can be overloaded by the application.
        """
        cls = self.__class__
        for super_class in self.db._sql_inherits(self.fqtn):
            self.db.table(super_class)
        dirname = os.path.dirname(os.path.abspath(inspect.getfile(cls)))
        templates_dir = "{}/cog/templates".format(dirname)
        ltd = []
        if templates_dir.find('/collorg/db/') != -1:
            rel_templates_dir = templates_dir.split('/collorg/db')[1]
            ltd.append("collorg/db{}".format(
                rel_templates_dir))
            app_template_dir = "collorg_app/{}/db/collorg{}".format(
                self.db.name, rel_templates_dir)
            ltd.append(app_template_dir)
        else:
            rel_templates_dir = templates_dir.split(
                '/collorg_app/{}/db'.format(self.db.name))[1]
            ltd.append("collorg_app/{}/db{}".format(
                self.db.name, rel_templates_dir))
        for app_templates_dir in ltd:
            templates_path = app_templates_dir.replace("/", ".")
            temp = None
            try:
                temp = __import__(
                    templates_path, locals(), globals(), ['*'], -1)
            except:
                pass
            if temp:
                for key, val in temp.__dict__.items():
                    if inspect.ismodule(val):
                        setattr(self.__class__, key, val.__dict__[key])
        self.__class__._templates_imported = True

    def __init__(self, _db, load_fields = True, trace = False, *args, **kwargs):
        Relation.__init__(self, _db)
        if not '_templates_imported' in self.__class__.__dict__:
            self.__import_templates()
        self.__neg_intention = False
        self.__extension = []
        self.__l_fields = []
        self._cog_order_by = []
        self.__retrieved = False
        self.__uniq = False
        self.__pkey_fields = []
        self.__label_fields = []
        self.__neighbors = self.db.neighbors(self.fqtn)
        self.__fields_loaded = load_fields
        if load_fields:
            self.__load_fields()
        if kwargs:
            for fieldname, val in kwargs.items():
                try:
                    self.__dict__[fieldname].set_intention(val)
                except Exception as err:
                    raise ValueError("%s Field %s error:\n'%s'\n" % (
                        self.name, fieldname, err))
        for field in args:
            self.__dict__[field.name].set_intention(field.val, field.comp)

    @property
    def _cog_description(self):
        oid = self.db.metadata.d_fqtn_table[self.fqtn]
        return self.db.metadata.d_oid_table[oid]['description']

    @property
    def _cog_pkey_fields(self):
        for field in self.__pkey_fields:
            yield field

    @property
    def _cog_label_fields(self):
        for field in self.__label_fields:
            yield field
        
    @property
    def _cog_inherits(self):
        """returns the list of objects inherited by self"""
        return self.__class__.__bases__
#        return self._cog_controller._cog_inherits(self)

    @property
    def _cog_fqtn_inherits(self):
        l_fqtn = []
        for elt in self._cog_inherits:
            if elt is Table:
                continue
            if hasattr(elt, '_cog_schemaname'):
                if elt is not self.__class__:
                    fqtn = "%s.%s" % (elt._cog_schemaname, elt._cog_tablename)
                l_fqtn.append(fqtn)
        return l_fqtn

    @property
    def cog_table(self):
        namespace = self.db.table(
            'collorg.core.namespace', name_ = self._cog_schemaname)
        table = namespace._rev_data_type_
        return table

    def has_field(self, fieldname):
        return fieldname in self.__dict__

    @property
    def retrieved(self):
        return self.__retrieved

    @property
    def uniq(self):
        return self.__uniq
    
    def _not_retrieved(self):
        self.__uniq = False
        self.__retrieved = False

    @property
    def schemaname(self):
        return self._cog_schemaname

    @property
    def name(self):
        return self._cog_tablename
    
    @property
    def neighbors(self):
        return self.__neighbors

    @property
    def rev_neighbors(self):
        return self.db.rev_neighbors(self.fqtn)

    def _is_linked_to(self, obj):
        return obj.fqtn in self.__neighbors

    def __call__(self, *args, **kwargs):
        if not self.__fields_loaded:
            self.__load_fields()
        return self.__class__(self.db, *args, **kwargs)

    # SQL substitutes

    def insert(self, just_return_sql = False):
        if self.db.test_mode and self.has_field('cog_test_'):
            self.cog_test_.set_intention(True)
            self.cog_signature_.set_intention(id(self.db))
        sql_req, cog_oid = self._cog_new_insert()
        if just_return_sql:
            return sql_req
        try:
            self.db.raw_sql(sql_req)
        except Exception as e:
            self.db.rollback()
            raise CustomError("Insert error: %s\n%s" % (e, sql_req))
        if cog_oid:
            # FORCE DATA RELOAD !!!
            i = 0
            while i < 5:
                time.sleep(0.01)
                i += 1
                try:
                    this = self.db.table(self.fqtn)
                    this.cog_oid_.set_intention(cog_oid)
                    self = this.get()
                    break
                except:
                    pass
        return self

    def __sql_delete(self, no_clause):
        """
        TEST CONSTRUCTION REQUETE SELECT. SANS DOUTE PAS ICI!!
        """
        req = ["DELETE"]
        req.append("FROM\n%s" % (self._cog_get_from()))
        if self._cog_is_constrained():
            req.append(self._cog_get_where())
        else:
            if not no_clause:
                raise Exception(
                    "Attempting to delete all tuples without no_clause!")
        return "\n".join(req)

    def _cog_delete(self, orig, just_return_sql, no_clause):
        sql_req = []
        if self._cog_base_table:
            oid = self.db.table('collorg.core.oid_table')
            oid.cog_oid_.set_intention(self.cog_oid_)
            sql_req.append(oid.delete(just_return_sql = True))
        if just_return_sql:
            no_clause = True
        sql_req.append(self.__sql_delete(no_clause = no_clause))
        if just_return_sql:
            return ";\n".join(sql_req)
        try:
            self.db.raw_sql(";\n".join(sql_req))
        except Exception as e:
            self.db.rollback()
            raise CustomError("Delete error:%s\n%s" % (e, sql_req))
        #!! à quoi bon retourner l'objet supprimé?
        return self

    def delete(self, just_return_sql = False, no_clause = False):
        return self._cog_delete(
            orig = self,
            just_return_sql = just_return_sql,
            no_clause = no_clause)

    def __sql_update(self, new_, no_clause = False):
        assert self.__class__ is new_.__class__
        l_fields = []
        clause = False
        for field in new_._cog_fields:
            if field.is_constrained:
                clause = True
                l_fields.append(field)
        what = ", ".join(
            ['"%s" = %s' % (field.name, field.quoted_val()) for field in l_fields])
        self.__sql = "UPDATE %s SET %s" % (new_.sql_fqtn, what)
        l_fields = []
        for field in self._cog_fields:
            if field.is_constrained:
                clause = True
                l_fields.append(field)
        where_fields = "(\n %s)" % ", ".join(
            ['"{}"'.format(field.name) for field in l_fields])
        if clause:
            self.__sql += " WHERE %s IN (\n %s)" % (
                where_fields,
                self.get_extent(
                    fields = l_fields, just_return_sql = True))
        else:
            if not no_clause:
                raise CustomError("Attempting to delete all tuples from %s" % (
                        self.sql_fqtn))
        return self.__sql.strip()
        
    def _cog_update(
        self, update_tuple, just_return_sql, no_clause,
        update_modif_date = True):
        """
        met à jour le self avec les valeurs du n_self
        """
        if just_return_sql:
            no_clause = True
        if self.has_field('cog_modif_date_') and update_modif_date:
            update_tuple.cog_modif_date_.set_intention(datetime.now())
        sql_req = self.__sql_update(update_tuple, no_clause)
        if just_return_sql:
            return sql_req
        try:
            self.db.raw_sql(sql_req)
        except Exception as e:
            self.db.rollback()
            raise CustomError("Update error:%s\n%s" % (e, sql_req))
        ## màj. de update_tuple pour y intégrer les nouvelles valeurs
        for field in update_tuple._cog_fields:
            if field.is_constrained:
                self.__dict__["%s_" % (field.name)].set_intention(field.value)
        return self

    def update(
        self, update_tuple, just_return_sql = False, no_clause = False,
        update_modif_date = True):
        return self._cog_update(
            update_tuple, just_return_sql = just_return_sql,
            no_clause = no_clause, update_modif_date = update_modif_date)

    # goodies

    # REFACTORING

    @property
    def _cog_fields(self):
        """
        @return: An iterator over the fields of the self
        """
        for elt in self.__l_fields:
            if self.__dict__[elt].__class__ is Field:
                yield self.__dict__[elt]

    def is_(self, other):
        """returns true if all fields are equal"""
        if self.__class__ != other.__class__:
            return False
        for field in self._cog_fields:
            if field.val != other.__dict__[field.pyname].val:
                return False
        return True

    def dup(self, *args):
        """
        Duplicates self with the fields passed by args.
        If no argument is passed, all the fields are duplicated
        """
        raise NotImplementedError
        dup_obj = self.db.table(self.fqtn)
        if len(args) == 0:
            args = self._cog_fields
        for field in args:
            dup_obj.__dict__[field.pyname].set_intention(field)
        return dup_obj

    def showstruct(self):
        res = ["        fields list:"]
        l_fields = self.db.metadata.fields_names(
            self._cog_schemaname, self._cog_tablename)
        for fieldname in l_fields:
            fref = self.db._metadata.\
                metadata[self._cog_schemaname]['d_tbl']\
                [self._cog_tablename]['d_fld'][fieldname]
            machin = []
            machin.append(fref['fieldtype'])
            fref["inherited"] and machin.append("inherited")
            fref['pkey'] and machin.append("PK")
            fref['uniq'] and machin.append("uniq")
            fref['notnull'] and machin.append("not null")
            fref['fkeyname'] and machin.append("FK")
            res_line = "        * %s_ : %s"
            res.append(res_line % (fieldname, ", ".join(machin)))
        return res
