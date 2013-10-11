#-*- coding: utf-8 -*-

from collorg.orm.table import Table

class A_function_inst_group( Table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.actor'
    _cog_tablename = 'a_function_inst_group'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _function_ = cog_r._function_
    _inst_group_ = cog_r._inst_group_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * function_ : c_oid, PK, not null, FK
        * inst_group_ : c_oid, PK, not null, FK
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( A_function_inst_group, self ).__init__( db, **kwargs )

