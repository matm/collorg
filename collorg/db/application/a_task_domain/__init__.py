#-*- coding: utf-8 -*-

from collorg.orm.table import Table

class A_task_domain( Table ):
    def __init__( self, db, **kwargs ):
        super( A_task_domain, self ).__init__( db, **kwargs )
