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

from collorg.db.core.oid_table import Oid_table
from collorg.orm.table import Table as TClass

class Base_table(Oid_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'base_table'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _cog_environment_ = cog_r._cog_environment_
    #<<< AUTO_COG REL_PART. Your code goes after
    _cog_base_table = True
    _cog_abstract_table = True
    _is_cog_post = False
    _is_cog_folder = False
    _is_cog_unit = False
    _is_cog_user = False
    _is_cog_group = False
    d_members = {}
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, PK, uniq, not null
        * cog_fqtn_ : c_fqtn, PK, not null
        * cog_signature_ : text
        * cog_test_ : bool
        * cog_creat_date_ : timestamp
        * cog_modif_date_ : timestamp
        * cog_environment_ : c_oid, FK
        * cog_state_ : text
        """
        #<<< AUTO_COG DOC. Your code goes after
        self._cog_order_by = []
        TClass.__init__( self, db, **kwargs )

    def get( self, fields = None, just_return_sql = False, recurse = True,
            reload_ = False):
        if not self.fqtn in [ 'collorg.core.base_table', 'collorg.core.oid_table' ]:
            return TClass.get(
                self,
                fields = fields, just_return_sql = just_return_sql,
                reload_ = reload_, recurse = recurse )
        obj = TClass.get(
            self, fields = fields, just_return_sql = just_return_sql,
            reload_ = reload_)
        if just_return_sql:
            return obj
        return self.db.table(
            self.cog_fqtn_.val, cog_oid_ = self.cog_oid_.val ).get(
                reload_ = reload_)

    @property
    def cog_type(self):
        """
        returns a 'collorg.core.data_type' with fqtn_ = self.cog_fqtn_
        """
        table = self.db.table('collorg.core.data_type')
        table.fqtn_.set_intention(self.fqtn)
        return table

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

    def cog_convert_to_bt(self):
        obt = Base_table(self.db)
        for field in obt._cog_fields:
            obt.__dict__[field.pyname] = self.__dict__[field.pyname]
        return obt

    def cog_path(self, data):
        try:
            return eval("data.{}".format(self._cog_paths[data.fqtn]))
        except KeyError:
            raise RuntimeError("Missing path between {} and {}".format(
                data.fqtn, self.fqtn))

    # RELATIONAL

    @property
    def members(self):
        # copy of core.oid_table.Oid_table.members
        access = self._rev_access_.granted()
        users = access._user_
        if self._rev_hierarchy_parent_.exists():
            for child in self._rev_hierarchy_parent_._child_:
                users += child.members
        return users

    def get_root_topic(self):
        return self.db.table('collorg.web.topic').get_root(self)

    def get_environment(self):
        if self.fqtn == 'collorg.web.topic':
            return self._cog_environment_
        return self
