# REVERSE
@property
def _rev_a_task_goal_(self):
    elt = self.db.table('collorg.application.a_task_goal')
    elt._goal_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

