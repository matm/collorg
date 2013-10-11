#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Transition( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'transition'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _action_ = cog_r._action_
    _start_state_ = cog_r._start_state_
    _end_state_ = cog_r._end_state_
    # REVERSE
    _rev_log_ = cog_r._rev_log_
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
        * name_ : string, not null
        * description_ : wiki
        * action_ : c_oid, not null, FK
        * start_state_ : c_oid, PK, not null, FK
        * end_state_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Transition, self ).__init__( db, **kwargs )
