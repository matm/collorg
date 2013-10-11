#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class A_wg_template_role( Base_table ):
    def __init__( self, db, **kwargs ):
        super( A_wg_template_role, self ).__init__( db, **kwargs )
