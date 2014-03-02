# DIRECT
def _get_granted(self):
    granted_ = self.db.table('collorg.core.oid_table')
    granted_.cog_oid_.value = self.granted_
    return granted_
def _set_granted(self, granted_):
    self.granted_.value = granted_.cog_oid_

_granted_ = property(
    _get_granted, _set_granted)

def _get_grants(self):
    grants_ = self.db.table('collorg.core.oid_table')
    grants_.cog_oid_.value = self.grants_
    return grants_
def _set_grants(self, grants_):
    self.grants_.value = grants_.cog_oid_

_grants_ = property(
    _get_grants, _set_grants)

