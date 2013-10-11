#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Url( Base_table ):
    def __init__( self, db, **kwargs ):
        super( Url, self ).__init__( db, **kwargs )
