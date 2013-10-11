#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class State( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'state'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_type_ = cog_r._data_type_
    # REVERSE
    _rev_transition_start_state_ = cog_r._rev_transition_start_state_
    _rev_transition_end_state_ = cog_r._rev_transition_end_state_
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
        * value_ : string, PK, not null
        * description_ : wiki
        * data_type_ : c_fqtn, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( State, self ).__init__( db, **kwargs )
