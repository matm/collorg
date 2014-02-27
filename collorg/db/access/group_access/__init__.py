#-*- coding: UTF-8 -*-

from datetime import datetime
from collorg.db.core.base_table import Base_table
from collorg.db.time.duration import Duration

class Group_access(Base_table, Duration):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access'
    _cog_tablename = 'group_access'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _group_data_ = cog_r._group_data_
    _accessed_data_ = cog_r._accessed_data_
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
        * cog_from_ : timestamp, inherited
        * cog_to_ : timestamp, inherited
        * group_data_ : c_oid, PK, not null, FK
        * accessed_data_ : c_oid, PK, not null, FK
        * begin_date_ : timestamp, PK, not null
        * end_date_ : timestamp
        * write_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Group_access, self).__init__(db, **kwargs)

    def granted(self, write=None):
        self.begin_date_.set_intention( datetime.now(), '<' )
        self.end_date_.set_null()
        self.end_date_ += ( datetime.now(), '>' )
        self.write_.set_intention(write)
        return self
