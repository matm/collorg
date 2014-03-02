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

from collorg.orm.table import Table as TClass

class Oid_table( TClass ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'oid_table'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_a_tag_post_ = cog_r._rev_a_tag_post_
    _rev_hierarchy_parent_ = cog_r._rev_hierarchy_parent_
    _rev_hierarchy_child_ = cog_r._rev_hierarchy_child_
    _rev_task_scheduler_ = cog_r._rev_task_scheduler_
    _rev_base_table_ = cog_r._rev_base_table_
    _rev_indirect_granted_ = cog_r._rev_indirect_granted_
    _rev_indirect_grants_ = cog_r._rev_indirect_grants_
    _rev_log_ = cog_r._rev_log_
    _rev_rss_ = cog_r._rev_rss_
    _rev_group_ = cog_r._rev_group_
    _rev_access_ = cog_r._rev_access_
    _rev_group_access_group_data_ = cog_r._rev_group_access_group_data_
    _rev_group_access_accessed_data_ = cog_r._rev_group_access_accessed_data_
    _rev_user_check_ = cog_r._rev_user_check_
    _rev_bookmark_ = cog_r._rev_bookmark_
    _rev_attachment_ = cog_r._rev_attachment_
    _rev_a_post_data_post_ = cog_r._rev_a_post_data_post_
    _rev_a_post_data_data_ = cog_r._rev_a_post_data_data_
    _rev_translation_ = cog_r._rev_translation_
    _rev_poll_ = cog_r._rev_poll_
    _rev_comment_ = cog_r._rev_comment_
    #<<< AUTO_COG REL_PART. Your code goes after
    __d_members_queries = {}
    _is_of_type_post = False
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, PK, uniq, not null
        * cog_fqtn_ : c_fqtn, PK, not null
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Oid_table, self ).__init__( db, **kwargs )

    def get(self, just_return_sql = False, reload_ = False):
        self = super(Oid_table, self).get(
            just_return_sql = just_return_sql, reload_ = reload_)
        obj = self.db.table(self.cog_fqtn_.value)
        obj.cog_oid_.set_intention(self.cog_oid_.value)
        return obj.get(just_return_sql = just_return_sql, reload_ = reload_)

    @property
    def members(self):
        #XXX TIME EXPENSIVE we store the queries in a class dictionary
        if not self.cog_oid_.value in Oid_table.__d_members_queries:
            users = self._rev_access_._user_
            if self._rev_hierarchy_parent_.exists():
                for child in self._rev_hierarchy_parent_._child_:
                    users += child.members
            Oid_table.__d_members_queries[self.cog_oid_.value] = users
        return Oid_table.__d_members_queries[self.cog_oid_.value]

    def get_base_topic(self):
        """
        #XXX TO MOVE IN collorg.communication.blog.post when...
        returns self if self is a topic, otherwise returns to the first
        topic in which self or a parent of self is posted.
        """
        print("fqtn: {}".format(self.fqtn))
        assert self.is_cog_post
        if self.fqtn == 'collorg.web.topic':
            return self
        return self._rev_a_post_data_post_._data_.get().get_base_topic()

    @property
    def is_cog_post(self):
        return hasattr(self, '_is_cog_post')

    @property
    def is_cog_event(self):
        return hasattr(self, '_is_cog_event')

    def _wipe_cache(self):
        for obj in self:
            if obj.__class__ == Oid_table:
                obj = obj.get()
            if obj._is_cog_post:
                return obj._wipe_cache()

