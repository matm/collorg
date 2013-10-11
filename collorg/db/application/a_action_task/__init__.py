#-*- coding: utf-8 -*-

from collorg.orm.table import Table

class A_action_task( Table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'a_action_task'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _action_ = cog_r._action_
    _task_ = cog_r._task_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * action_ : c_oid, PK, not null, FK
        * task_ : c_oid, PK, not null, FK
        * delegable_ : bool
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( A_action_task, self ).__init__( db, **kwargs )
