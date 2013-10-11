#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class User_check(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'user_check'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _communication_object_ = cog_r._communication_object_
    _user_ = cog_r._user_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * communication_object_ : c_oid, PK, not null, FK
        * user_ : c_oid, PK, not null, FK
        * date_checked_ : timestamp
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(User_check, self).__init__(db, **kwargs)

