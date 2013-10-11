#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Membership(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.group.view'
    _cog_tablename = 'membership'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * user_oid_ : c_oid
        * first_name_ : string
        * last_name_ : string
        * email_ : email
        * group_oid_ : c_oid
        * access_from_ : timestamp
        * access_to_ : timestamp
        * function_oid_ : c_oid
        * function_name_ : string
        * function_long_name_ : string
        * function_advertise_ : bool
        * data_oid_ : c_oid
        * data_fqtn_ : c_fqtn
        * group_name_ : string
        * role_from_ : timestamp
        * role_to_ : timestamp
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Membership, self).__init__(db, **kwargs)

