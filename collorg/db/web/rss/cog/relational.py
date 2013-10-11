# DIRECT
def _get_user(self):
    user_ = self.db.table('collorg.core.oid_table')
    user_.cog_oid_.set_intention(self.user_)
    return user_
def _set_user(self, user_):
    self.user_.set_intention(user_.cog_oid_)

_user_ = property(
    _get_user, _set_user)

# REVERSE
@property
def _rev_a_rss_topic_(self):
    elt = self.db.table('collorg.web.a_rss_topic')
    elt._rss_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

