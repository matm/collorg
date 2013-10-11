#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class Address(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.location'
    _cog_tablename = 'address'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_building_ = cog_r._rev_building_
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
        * address_id_ : c_oid
        * line_1_ : string, not null
        * line_2_ : string
        * line_3_ : string
        * city_ : string, not null
        * county_province_ : string
        * zip_or_postcode_ : string
        * country_ : string, not null
        * other_address_details_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Address, self).__init__(db, **kwargs)

