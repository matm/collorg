#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Topic_graph(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'topic_graph'
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
        * order_ : int4
        * link_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Topic_graph, self).__init__(db, **kwargs)

