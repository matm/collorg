# DIRECT
def _get_cog_environment(self):
    cog_environment_ = self.db.table('collorg.core.oid_table')
    cog_environment_.cog_oid_.set_intention(self.cog_environment_)
    return cog_environment_
def _set_cog_environment(self, cog_environment_):
    self.cog_environment_.set_intention(cog_environment_.cog_oid_)

_cog_environment_ = property(
    _get_cog_environment, _set_cog_environment)

