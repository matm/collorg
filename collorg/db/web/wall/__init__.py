#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Wall(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'wall'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _topic_ = cog_r._topic_
    _parent_ = cog_r._parent_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * topic_ : c_oid, PK, not null, FK
        * parent_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Wall, self).__init__(db, **kwargs)

