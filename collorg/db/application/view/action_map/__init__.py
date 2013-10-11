#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Action_map(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application.view'
    _cog_tablename = 'action_map'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * function_oid_ : c_oid
        * function_name_ : string
        * goal_name_ : string
        * task_oid_ : c_oid
        * task_name_ : string
        * cog_oid_ : c_oid
        * name_ : string
        * in_menu_ : bool
        * label_ : string
        * fqtn_ : text
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Action_map, self).__init__(db, **kwargs)

