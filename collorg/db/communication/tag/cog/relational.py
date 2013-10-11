# REVERSE
@property
def _rev_a_tag_post_(self):
    elt = self.db.table('collorg.communication.a_tag_post')
    elt._tag_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

