#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table
from collorg.db.time.duration import Duration
from collorg.db.group._groupable import Groupable

#class Unit(Base_table, Duration, Groupable):
class Unit(Base_table, Groupable):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.organization'
    _cog_tablename = 'unit'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    collorg_organization_unit = True
    _cog_abstract_table = True
    _is_cog_unit = True
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, uniq, not null
        * cog_fqtn_ : c_fqtn, PK, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * cog_from_ : timestamp, inherited
        * cog_to_ : timestamp, inherited
        * acronym_ : string
        * name_ : string, PK, not null
        * description_ : wiki
        * url_ : url
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Unit, self ).__init__( db, **kwargs )

    @property
    def _cog_label(self):
        return ["{}", self.name_]

    def new(self, author):
        self.insert()
        topic = self.db.table('collorg.web.topic')
        topic.set_root(self, author)
        return self
