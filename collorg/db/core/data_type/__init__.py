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

from collorg.db.core.base_table import Base_table

class Data_type( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'data_type'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _namespace_ = cog_r._namespace_
    # REVERSE
    _rev_action_ = cog_r._rev_action_
    _rev_topic_data_type_ = cog_r._rev_topic_data_type_
    _rev_topic_post_type_ = cog_r._rev_topic_post_type_
    _rev_field_ = cog_r._rev_field_
    _rev_a_tag_post_ = cog_r._rev_a_tag_post_
    _rev_function_ = cog_r._rev_function_
    _rev_state_ = cog_r._rev_state_
    _rev_inst_group_ = cog_r._rev_inst_group_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, uniq, not null
        * cog_fqtn_ : c_fqtn, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * namespace_ : c_oid, PK, not null, FK
        * name_ : string, PK, not null
        * fqtn_ : text, uniq, not null
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Data_type, self ).__init__( db, **kwargs )


    def insert( self, **kwargs ):
        namespace = self.db.table( 'collorg.core.namespace' )
        namespace.name_.set_intention(self.fqtn_.value.rsplit( '.', 1 )[0])
        if not namespace.exists():
            self.db.set_auto_commit( False )
            namespace.insert()
        self._namespace_ = namespace
        super( Data_type, self ).insert( **kwargs )
        self.db.commit()

    def __call__( self ):
        assert self.fqtn_.value.__class__ is str
        return self.db.table( self.fqtn_.value )

    def __add_data_type_self_ref(self):
        fqtn = self.fqtn
        data_type = self.db.table(fqtn)
        data_type.fqtn_.set_intention(fqtn)
        data_type.name_.set_intention(fqtn.split(".")[-1])
        if not data_type.exists():
            print("+ adding %s in data_type" % fqtn)
            data_type.insert()
        self._rev_field_.add_new(fqtn)

    def _populate(self):
        self.__add_data_type_self_ref()
        for fqtn in self.db.fqtns:
            if fqtn == self.fqtn:
                continue
            data_type = self.db.table('collorg.core.data_type', fqtn_ = fqtn)
            data_type.fqtn_.set_intention(fqtn)
            data_type.name_.set_intention(fqtn.split(".")[-1])
            if data_type.count() == 0:
                print("+ adding %s in data_type" % fqtn)
                data_type.insert()
            try:
                data_type._rev_field_.add_new(fqtn)
            except:
                pass
