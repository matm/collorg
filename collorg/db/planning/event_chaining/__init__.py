#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Event_chaining( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.planning'
    _cog_tablename = 'event_chaining'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _event_ = cog_r._event_
    _next_event_ = cog_r._next_event_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : uuid, uniq, not null
        * cog_fqtn_ : text, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_presentation_ : wiki, inherited
        * cog_state_ : text, inherited
        * event_ : uuid, PK, not null, FK
        * critical_ : bool
        * next_event_ : uuid, PK, not null, FK
        * private_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Event_chaining, self ).__init__( db, **kwargs )

