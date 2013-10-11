#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Database( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'database'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_namespace_ = cog_r._rev_namespace_
    _rev_changelog_ = cog_r._rev_changelog_
    #<<< AUTO_COG REL_PART. Your code goes after
    _cog_label_fields = 'name_'
    def __init__( self, db, **kwargs ):
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
        * name_ : string, PK, not null
        * long_name_ : text, uniq
        * release_ : int4
        * sub_release_ : int4
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Database, self ).__init__( db, **kwargs )

