#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Children(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication.blog.view'
    _cog_tablename = 'children'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * parent_oid_ : c_oid
        * cog_oid_ : c_oid
        * cog_fqtn_ : c_fqtn
        * cog_creat_date_ : timestamp
        * cog_modif_date_ : timestamp
        * title_ : string
        * visibility_ : string
        * introductory_paragraph_ : string
        * public_ : bool
        * important_ : bool
        * broadcast_ : bool
        * expiry_date_ : timestamp
        * order_ : int4
        * author_oid_ : c_oid
        * author_first_name_ : string
        * author_last_name_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Children, self).__init__(db, **kwargs)

