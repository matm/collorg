# DIRECT
def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.set_intention(self.data_)
    return data_
def _set_data(self, data_):
    self.data_.set_intention(data_.cog_oid_)

_data_ = property(
    _get_data, _set_data)

def _get_user(self):
    user_ = self.db.table('collorg.actor.user')
    user_.cog_oid_.set_intention(self.user_)
    return user_
def _set_user(self, user_):
    self.user_.set_intention(user_.cog_oid_)

_user_ = property(
    _get_user, _set_user)

# REVERSE
@property
def _rev_role_(self):
    elt = self.db.table('collorg.access.role')
    elt._access_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

