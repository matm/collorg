# DIRECT
def _get_appointer(self):
    appointer_ = self.db.table('collorg.actor.role')
    appointer_.cog_oid_.set_intention(self.appointer_)
    return appointer_
def _set_appointer(self, appointer_):
    self.appointer_.set_intention(appointer_.cog_oid_)

_appointer_ = property(
    _get_appointer, _set_appointer)

def _get_appointee(self):
    appointee_ = self.db.table('collorg.actor.role')
    appointee_.cog_oid_.set_intention(self.appointee_)
    return appointee_
def _set_appointee(self, appointee_):
    self.appointee_.set_intention(appointee_.cog_oid_)

_appointee_ = property(
    _get_appointee, _set_appointee)

