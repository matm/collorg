#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class A_rss_topic(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'a_rss_topic'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _rss_ = cog_r._rss_
    _topic_ = cog_r._topic_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * rss_ : c_oid, FK
        * topic_ : c_oid, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(A_rss_topic, self).__init__(db, **kwargs)

