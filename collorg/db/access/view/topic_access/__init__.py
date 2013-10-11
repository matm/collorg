#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Topic_access(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access.view'
    _cog_tablename = 'topic_access'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * user_oid_ : c_oid
        * topic_oid_ : c_oid
        * access_from_ : timestamp
        * access_to_ : timestamp
        * function_oid_ : c_oid
        * write_ : bool
        * moderate_ : bool
        * admin_ : bool
        * topic_visibility_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Topic_access, self).__init__(db, **kwargs)

