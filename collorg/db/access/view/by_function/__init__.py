#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class By_function(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access.view'
    _cog_tablename = 'by_function'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid
        * pourcentage_ : int4
        * begin_date_ : timestamp
        * end_date_ : timestamp
        * write_ : bool
        * manage_ : bool
        * data_oid_ : c_oid
        * data_fqtn_ : c_fqtn
        * user_oid_ : c_oid
        * user_pseudo_ : text
        * user_first_name_ : string
        * user_last_name_ : string
        * function_oid_ : c_oid
        * function_name_ : string
        * function_long_name_ : string
        * function_advertise_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(By_function, self).__init__(db, **kwargs)

