#-*- coding: utf-8 -*-

from collorg.orm.table import Table

class A_user_category( Table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.actor'
    _cog_tablename = 'a_user_category'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _user_ = cog_r._user_
    _category_ = cog_r._category_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * user_ : c_oid, PK, not null, FK
        * category_ : c_oid, PK, not null, FK
        * begin_ : timestamp
        * end_ : timestamp
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( A_user_category, self ).__init__( db, **kwargs )

