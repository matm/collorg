#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Changelog(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core.patch'
    _cog_tablename = 'changelog'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _database_ = cog_r._database_
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
        * major_ : int4, PK, not null
        * minor_ : int4, PK, not null
        * stage_ : int4, PK, not null
        * revision_ : int4, PK, not null
        * database_ : c_oid, PK, not null, FK
        * label_ : string, not null
        * description_ : wiki
        * output_ : text
        * error_ : text
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Changelog, self).__init__(db, **kwargs)

