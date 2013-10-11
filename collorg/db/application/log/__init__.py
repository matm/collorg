#-*- coding: utf-8 -*-

from collorg.orm.table import Table

class Log(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'log'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _action_ = cog_r._action_
    _state_ = cog_r._state_
    _data_oid_ = cog_r._data_oid_
    _user_ = cog_r._user_
    _transition_ = cog_r._transition_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * id_ : int4, PK, not null
        * timestamp_ : timestamp
        * action_ : c_oid, not null, FK
        * data_oid_ : c_oid, FK
        * transition_ : c_oid, FK
        * state_ : c_oid, FK
        * user_ : c_oid, FK
        * log_text_ : text
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Log, self ).__init__( db, **kwargs )
