# DIRECT
def _get_error(self):
    error_ = self.db.table('collorg.application.communication.error')
    error_.cog_oid_.set_intention(self.error_)
    return error_
def _set_error(self, error_):
    self.error_.set_intention(error_.cog_oid_)

_error_ = property(
    _get_error, _set_error)

