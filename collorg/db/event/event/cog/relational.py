# DIRECT
def _get_location(self):
    location_ = self.db.table('collorg.location.room')
    location_.cog_oid_.set_intention(self.location_)
    return location_
def _set_location(self, location_):
    self.location_.set_intention(location_.cog_oid_)

_location_ = property(
    _get_location, _set_location)

