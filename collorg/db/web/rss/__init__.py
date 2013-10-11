#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Rss(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'rss'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _user_ = cog_r._user_
    # REVERSE
    _rev_a_rss_topic_ = cog_r._rev_a_rss_topic_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * key_ : c_oid, uniq, not null
        * user_ : c_oid, PK, not null, FK
        * title_ : string, PK, not null
        * description_ : text
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Rss, self).__init__(db, **kwargs)

