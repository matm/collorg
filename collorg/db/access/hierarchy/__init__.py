#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class Hierarchy(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access'
    _cog_tablename = 'hierarchy'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _parent_ = cog_r._parent_
    _child_ = cog_r._child_
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
        * parent_ : c_oid, PK, not null, FK
        * child_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Hierarchy, self).__init__(db, **kwargs)

