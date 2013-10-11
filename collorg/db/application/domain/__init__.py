#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Domain( Base_table ):
    def __init__( self, db, **kwargs ):
        super( Domain, self ).__init__( db, **kwargs )
