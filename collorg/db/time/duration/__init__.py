#-*- coding: UTF-8 -*-

from datetime import datetime
from collorg.orm.table import Table

class Duration(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.time'
    _cog_tablename = 'duration'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_from_ : timestamp
        * cog_to_ : timestamp
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Duration, self).__init__(db, **kwargs)

    def granted( self ):
        self.cog_from_.set_intention( datetime.now(), '<' )
        self.cog_to_.set_null()
        self.cog_to_ += ( datetime.now(), '>' )
        return self
