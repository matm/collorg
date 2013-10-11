#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Bookmark(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'bookmark'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _post_ = cog_r._post_
    _user_ = cog_r._user_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * post_ : c_oid, PK, not null, FK
        * user_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Bookmark, self).__init__(db, **kwargs)

    def winsert(self, **kwargs):
        assert kwargs['user_oid'] and kwargs['post_oid']
        self.user_.set_intention(kwargs['user_oid'])
        self.post_.set_intention(kwargs['post_oid'])
        if not self.exists():
            self.insert()
