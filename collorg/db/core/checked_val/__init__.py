#-*- coding: utf-8 -*-

#>>>> do not edit the following lines

from collorg.db.core.base_table import Base_table

class Checked_val( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core'
    _cog_tablename = 'checked_val'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _field_ = cog_r._field_
    # REVERSE
    _rev_d_ldap_connectivity_security_ = cog_r._rev_d_ldap_connectivity_security_
    _rev_d_ldap_certificate_checks_ = cog_r._rev_d_ldap_certificate_checks_
    _rev_d_ldap_scope_ = cog_r._rev_d_ldap_scope_
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
        * field_ : string, PK, not null, FK
        * val_ : string, PK, not null
        * default_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Checked_val, self ).__init__( db, **kwargs )

    #<<<< do not edit the preceding lines
