# REVERSE
@property
def _rev_namespace_(self):
    elt = self.db.table('collorg.core.namespace')
    elt._database_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_changelog_(self):
    elt = self.db.table('collorg.core.patch.changelog')
    elt._database_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

