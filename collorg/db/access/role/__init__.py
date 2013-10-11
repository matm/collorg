#-*- coding: UTF-8 -*-

from datetime import datetime
from collorg.db.core.base_table import Base_table
from collorg.db.time.duration import Duration

class Role(Base_table, Duration):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access'
    _cog_tablename = 'role'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _function_ = cog_r._function_
    _access_ = cog_r._access_
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
        * cog_from_ : timestamp, PK, not null
        * cog_to_ : timestamp, inherited
        * access_ : c_oid, PK, not null, FK
        * function_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Role, self).__init__(db, **kwargs)

    def grant(self, cog_from_ = None, cog_to_ = None):
        """
        self must be constrained by an access_ and a function_ before grant is
        called:
            role.access_ = access
            role.function_ = function
        @begin_date: optional (defaults to now())
        @end_date: optional
        """
        self.cog_from_.set_intention(cog_from_)
        self.cog_to_.set_intention(cog_to_)
        if not self.is_granted():
            self.insert()

    def is_granted(self):
        if not self.exists():
            return False
        role = self()
        role.cog_oid_.set_intention(self.cog_oid_)
        role.cog_from_.set_intention(datetime.now(), '<=')
        role.cog_to_.set_null()
        role.cog_to_ += (datetime.now(), '>')
        return role.exists()

    def revoke(self, no_access = False, no_function = False):
        assert no_access or self.access_.is_constrained
        assert no_function or self.function_.is_constrained
        for elt in self:
            n_role = self()
            n_role.cog_to_.set_intention(datetime.now())
            elt.update(n_role)
