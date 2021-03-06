#-*- coding: utf-8 -*-

#>>>> do not edit the following lines

from collorg.orm.table import Table

class A_task_goal( Table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'a_task_goal'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _task_ = cog_r._task_
    _goal_ = cog_r._goal_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * task_ : c_oid, PK, not null, FK
        * goal_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( A_task_goal, self ).__init__( db, **kwargs )

    #<<<< do not edit the preceding lines
