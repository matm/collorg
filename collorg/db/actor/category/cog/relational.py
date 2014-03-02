# DIRECT
def _get_parent_oid(self):
    parent_oid_ = self.db.table('collorg.actor.category')
    parent_oid_.cog_oid_.value = self.parent_oid_
    return parent_oid_
def _set_parent_oid(self, parent_oid_):
    self.parent_oid_.value = parent_oid_.cog_oid_

_parent_oid_ = property(
    _get_parent_oid, _set_parent_oid)

# REVERSE
@property
def _rev_a_function_category_(self):
    elt = self.db.table('collorg.actor.a_function_category')
    elt._category_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_a_user_category_(self):
    elt = self.db.table('collorg.actor.a_user_category')
    elt._category_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_category_(self):
    elt = self.db.table('collorg.actor.category')
    elt._parent_oid_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

