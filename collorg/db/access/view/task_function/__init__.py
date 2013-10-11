#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Task_function(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access.view'
    _cog_tablename = 'task_function'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * task_name_ : string
        * function_name_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Task_function, self).__init__(db, **kwargs)

