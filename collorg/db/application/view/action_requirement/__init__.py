#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Action_requirement(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application.view'
    _cog_tablename = 'action_requirement'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * requires_oid_ : c_oid
        * requires_name_ : string
        * requires_data_type_ : c_fqtn
        * required_oid_ : c_oid
        * required_name_ : string
        * required_data_type_ : c_fqtn
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Action_requirement, self).__init__(db, **kwargs)
