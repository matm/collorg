# DIRECT
def _get_connectivity_security(self):
    connectivity_security_ = self.db.table('collorg.core.checked_val')
    connectivity_security_.cog_oid_.set_intention(self.connectivity_security_)
    return connectivity_security_
def _set_connectivity_security(self, connectivity_security_):
    self.connectivity_security_.set_intention(connectivity_security_.cog_oid_)

_connectivity_security_ = property(
    _get_connectivity_security, _set_connectivity_security)

def _get_certificate_checks(self):
    certificate_checks_ = self.db.table('collorg.core.checked_val')
    certificate_checks_.cog_oid_.set_intention(self.certificate_checks_)
    return certificate_checks_
def _set_certificate_checks(self, certificate_checks_):
    self.certificate_checks_.set_intention(certificate_checks_.cog_oid_)

_certificate_checks_ = property(
    _get_certificate_checks, _set_certificate_checks)

def _get_scope(self):
    scope_ = self.db.table('collorg.core.checked_val')
    scope_.cog_oid_.set_intention(self.scope_)
    return scope_
def _set_scope(self, scope_):
    self.scope_.set_intention(scope_.cog_oid_)

_scope_ = property(
    _get_scope, _set_scope)

# REVERSE
@property
def _rev_user_(self):
    elt = self.db.table('collorg.actor.user')
    elt._ldap_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

