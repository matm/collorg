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

class CustomError( Exception ):
    pass

class Action(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'action'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_type_ = cog_r._data_type_
    # REVERSE
    _rev_topic_ = cog_r._rev_topic_
    _rev_log_ = cog_r._rev_log_
    _rev_a_action_task_ = cog_r._rev_a_action_task_
    _rev_transition_ = cog_r._rev_transition_
    _rev_check_requires_ = cog_r._rev_check_requires_
    _rev_check_required_ = cog_r._rev_check_required_
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
        * data_type_ : c_fqtn, PK, not null, FK
        * name_ : string, PK, not null
        * label_ : string
        * description_ : wiki
        * format_ : string
        * source_ : text
        * raw_ : bool
        * protected_ : bool
        * in_menu_ : bool
        * in_header_ : bool
        * in_nav_ : bool
        * write_ : bool
        * moderate_ : bool
        * admin_ : bool
        * icon_ : string
        * this_application_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Action, self ).__init__( db, **kwargs )

    @property
    def _cog_label(self):
        return ["{}",self.label_]

    def link_to_task( self, task ):
        #print( "%s\n%s" % ( self._cog_debug, task._cog_debug ) )
        if not self.cog_oid_.value:
            self.get()
        if not task.cog_oid_.value:
            task.get()
        aat = self.db.table( 'collorg.application.a_action_task' )
        aat.action_ = self
        aat.task_ = task
        if not aat.exists():
            print("+ new assoc action<->task: %s<->%s" % (
                self.name_.value, task.name_.value))
            aat.insert()

    def is_granted(self, obj):
        """
        obj is a topic.
        """
        return True
#        atf = obj.get_a_topic_function()
#        if not atf.exists():
#            return True
#        if self.write_.value or self.moderate_.value or self.admin_.value:
#            atf.write_.value = self.write_.value
#            atf.moderate_.value = self.moderate_.value
#            atf.admin_.value = self.admin_.value
#            atf *= self._cog_controller.user._rev_access_.\
#                _rev_role_._function_._rev_a_topic_function_
#            return atf.exists()
#        return True
