# REVERSE
@property
def _rev_error_traceback_(self):
    elt = self.db.table('collorg.application.communication.error_traceback')
    elt._error_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

