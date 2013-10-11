#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Category( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.actor'
    _cog_tablename = 'category'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _parent_oid_ = cog_r._parent_oid_
    # REVERSE
    _rev_a_function_category_ = cog_r._rev_a_function_category_
    _rev_a_user_category_ = cog_r._rev_a_user_category_
    _rev_category_ = cog_r._rev_category_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
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
        * label_ : string, uniq, not null
        * parent_oid_ : c_oid, uniq, FK
        * expiry_date_ : date
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Category, self ).__init__( db, **kwargs )

