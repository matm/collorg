#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class Task_schedule(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.planning'
    _cog_tablename = 'task_schedule'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _schedule_oid_ = cog_r._schedule_oid_
    _schedule_fqtn_ = cog_r._schedule_fqtn_
    _task_ = cog_r._task_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : uuid, uniq, not null
        * cog_fqtn_ : text, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_presentation_ : wiki, inherited
        * cog_state_ : text, inherited
        * task_ : uuid, PK, not null, FK
        * schedule_oid_ : uuid, PK, not null, FK
        * schedule_fqtn_ : string, not null, FK
        * editable_ : string
        * original_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Task_schedule, self).__init__(db, **kwargs)

