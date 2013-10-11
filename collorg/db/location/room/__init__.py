#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class Room(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.location'
    _cog_tablename = 'room'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _building_ = cog_r._building_
    # REVERSE
    _rev_event_ = cog_r._rev_event_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, uniq, not null
        * cog_fqtn_ : c_fqtn, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * name_ : string
        * building_ : c_oid, FK
        * access_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Room, self).__init__(db, **kwargs)

