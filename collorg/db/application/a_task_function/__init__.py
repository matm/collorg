#-*- coding: utf-8 -*-

from collorg.orm.table import Table

class A_task_function( Table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'a_task_function'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _function_ = cog_r._function_
    _task_ = cog_r._task_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * function_ : c_oid, PK, not null, FK
        * task_ : c_oid, PK, not null, FK
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( A_task_function, self ).__init__( db, **kwargs )

