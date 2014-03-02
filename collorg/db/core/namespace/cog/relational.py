# DIRECT
def _get_database(self):
    database_ = self.db.table('collorg.core.database')
    database_.cog_oid_.value = self.database_
    return database_
def _set_database(self, database_):
    self.database_.value = database_.cog_oid_

_database_ = property(
    _get_database, _set_database)

# REVERSE
@property
def _rev_data_type_(self):
    elt = self.db.table('collorg.core.data_type')
    elt._namespace_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

