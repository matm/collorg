#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Poll(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'poll'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _post_ = cog_r._post_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * shuffle_ : int4
        * post_ : c_oid, not null, FK
        * vote_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Poll, self).__init__(db, **kwargs)

