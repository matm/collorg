#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Group( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.group'
    _cog_tablename = 'group'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_ = cog_r._data_
    # REVERSE
    _rev_definition_ = cog_r._rev_definition_
    _rev_calendar_ = cog_r._rev_calendar_
    #<<< AUTO_COG REL_PART. Your code goes after
    _is_cog_group = True
    """
    A group is one of the two elements by which an access is granted
    to a user (collorg.actor.user). The other element is the role (collorg.actor.role).
    Five roles exist by default (see collorg.actor.role).
    By default, a group is created for each unit in the database to it (see
    collorg.organization.unit)
    """
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
        * name_ : string, PK, not null
        * data_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Group, self ).__init__( db, **kwargs )


    @property
    def _cog_label(self):
        return ["{} {}", self.name_, self._data_.get().cog_label()]

    @property
    def events(self):
        """
        returns the set of events attached to the group
        """
        return self._rev_calendar_._rev_a_event_calendar_._event_

    def __set_group_access(self, data, write):
        assert self.count() == 1 and data.count() == 1
        ga = self.db.table('collorg.access.group_access')
        ga._accessed_data_ = data
        ga._group_data_ = self
        ga.write_.set_intention(write)
        return ga

    def grant_access(self, data, write=False):
        ga = self.__set_group_access(data, write)
        if not ga.exists():
            ga.insert()

    def revoke_access(self, data):
        ga = self.__set_group_access(data)
        if ga.exists():
            ga.delete()

    def grant_write_access(self, data):
        ga = self.__set_group_access(data, False)
        nga = ga()
        nga.write_.set_intention(True)
        if ga.exists():
            ga.update(nga)

    def revoke_write_access(self, data):
        ga = self.__set_group_access(data, True)
        nga = ga()
        nga.write_.set_intention(False)
        if ga.exists():
            ga.update(nga)
