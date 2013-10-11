#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Definition(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.group'
    _cog_tablename = 'definition'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _function_ = cog_r._function_
    _group_ = cog_r._group_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * group_ : c_oid, PK, not null, FK
        * function_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Definition, self).__init__(db, **kwargs)

