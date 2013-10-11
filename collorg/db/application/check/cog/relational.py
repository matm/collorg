# DIRECT
def _get_requires(self):
    requires_ = self.db.table('collorg.application.action')
    requires_.cog_oid_.set_intention(self.requires_)
    return requires_
def _set_requires(self, requires_):
    self.requires_.set_intention(requires_.cog_oid_)

_requires_ = property(
    _get_requires, _set_requires)

def _get_required(self):
    required_ = self.db.table('collorg.application.action')
    required_.cog_oid_.set_intention(self.required_)
    return required_
def _set_required(self, required_):
    self.required_.set_intention(required_.cog_oid_)

_required_ = property(
    _get_required, _set_required)

