#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Inst_tag(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication.view'
    _cog_tablename = 'inst_tag'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * count_ : int8
        * tag_ : string
        * inst_tag_ : bool
        * data_type_ : c_fqtn
        * status_ : string
        * dt_description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Inst_tag, self).__init__(db, **kwargs)

