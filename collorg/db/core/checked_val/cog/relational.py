# DIRECT
def _get_field(self):
    field_ = self.db.table('collorg.core.field')
    field_.fqfn_.set_intention(self.field_)
    return field_
def _set_field(self, field_):
    self.field_.set_intention(field_.fqfn_)

_field_ = property(
    _get_field, _set_field)

# REVERSE
@property
def _rev_d_ldap_connectivity_security_(self):
    elt = self.db.table('collorg.auth.d_ldap')
    elt._connectivity_security_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_d_ldap_certificate_checks_(self):
    elt = self.db.table('collorg.auth.d_ldap')
    elt._certificate_checks_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_d_ldap_scope_(self):
    elt = self.db.table('collorg.auth.d_ldap')
    elt._scope_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

