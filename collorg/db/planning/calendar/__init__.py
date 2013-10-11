#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Calendar( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.planning'
    _cog_tablename = 'calendar'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _group_ = cog_r._group_
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
        * group_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Calendar, self ).__init__( db, **kwargs )

    @property
    def events(self):
        return self._rev_a_event_calendar_._event_
