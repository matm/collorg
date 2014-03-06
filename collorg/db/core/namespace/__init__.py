#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Namespace( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'namespace'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _database_ = cog_r._database_
    # REVERSE
    _rev_data_type_ = cog_r._rev_data_type_
    #<<< AUTO_COG REL_PART. Your code goes after
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
        * database_ : c_oid, PK, not null, FK
        * name_ : string, PK, not null
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Namespace, self ).__init__( db, **kwargs )

    def insert( self, db_name = None, **kwargs ):
        database = self.db.table( 'collorg.core.database' )
        database.name_.value =  db_name or self.db.name
        if database.is_empty():
            database.insert()
        self._database_ = database
        super( Namespace, self ).insert( **kwargs )
