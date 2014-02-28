# REVERSE
@property
def _rev_topic_(self):
    elt = self.db.table('collorg.web.topic')
    elt._site_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

