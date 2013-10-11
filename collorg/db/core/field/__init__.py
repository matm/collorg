#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Field( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'field'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_type_ = cog_r._data_type_
    # REVERSE
    _rev_checked_val_ = cog_r._rev_checked_val_
    _rev_translation_ = cog_r._rev_translation_
    _rev_comment_ = cog_r._rev_comment_
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
        * data_type_ : c_fqtn, not null, FK
        * fqfn_ : string, PK, not null
        * label_ : string
        * status_ : string
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Field, self ).__init__( db, **kwargs )

    def add_new(self, fqtn):
        """
        scans all the fiels of the db. adds the new ones
        """
        the_table = self.db.table(fqtn)
        for field in the_table._cog_fields:
            self.reset()
            self.data_type_.set_intention(fqtn)
            self.fqfn_.set_("%s.%s"%(fqtn, field.name))
            if not self.exists():
                print("+ %s.%s" % (fqtn, field.name))
                self.insert()
