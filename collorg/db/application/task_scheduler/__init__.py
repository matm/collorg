#-*- coding: UTF-8 -*-

from collorg.db.time.duration import Duration
from collorg.db.core.base_table import Base_table

class Task_scheduler(Duration, Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'task_scheduler'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_ = cog_r._data_
    _task_ = cog_r._task_
    _year_ = cog_r._year_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, PK, not null
        * cog_fqtn_ : c_fqtn, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * cog_from_ : timestamp, inherited
        * cog_to_ : timestamp, inherited
        * description_ : wiki
        * task_ : c_oid, not null, FK
        * year_ : int4, uniq, FK
        * data_ : c_oid, uniq, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Task_scheduler, self).__init__(db, **kwargs)

