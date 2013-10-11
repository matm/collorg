# DIRECT
def _get_uploader(self):
    uploader_ = self.db.table('collorg.actor.user')
    uploader_.cog_oid_.set_intention(self.uploader_)
    return uploader_
def _set_uploader(self, uploader_):
    self.uploader_.set_intention(uploader_.cog_oid_)

_uploader_ = property(
    _get_uploader, _set_uploader)

# REVERSE
@property
def _rev_attachment_(self):
    elt = self.db.table('collorg.communication.attachment')
    elt._ref_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_user_(self):
    elt = self.db.table('collorg.actor.user')
    elt._photo_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

