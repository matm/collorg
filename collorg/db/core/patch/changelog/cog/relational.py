# DIRECT
def _get_database(self):
    database_ = self.db.table('collorg.core.database')
    database_.cog_oid_.value = self.database_
    return database_
def _set_database(self, database_):
    self.database_.value = database_.cog_oid_

_database_ = property(
    _get_database, _set_database)

