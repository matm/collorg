#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Action_task(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access.view'
    _cog_tablename = 'action_task'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * task_name_ : string
        * action_name_ : string
        * data_fqtn_ : text
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Action_task, self).__init__(db, **kwargs)

