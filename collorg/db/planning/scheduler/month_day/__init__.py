#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class Month_day(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.planning.scheduler'
    _cog_tablename = 'month_day'
    _cog_templates_loaded = False

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
        * num_ : int4, PK, not null
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Month_day, self).__init__(db, **kwargs)

