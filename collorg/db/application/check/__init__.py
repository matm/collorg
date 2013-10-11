#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Check(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'check'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _requires_ = cog_r._requires_
    _required_ = cog_r._required_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * description_ : wiki
        * requires_ : c_oid, PK, not null, FK
        * required_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Check, self).__init__(db, **kwargs)
