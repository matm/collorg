#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class A_topic_function(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access'
    _cog_tablename = 'a_topic_function'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _topic_ = cog_r._topic_
    _function_ = cog_r._function_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * function_ : c_oid, PK, not null, FK
        * topic_ : c_oid, PK, not null, FK
        * write_ : bool
        * moderate_ : bool
        * admin_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(A_topic_function, self).__init__(db, **kwargs)

