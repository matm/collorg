# DIRECT
def _get_building(self):
    building_ = self.db.table('collorg.location.building')
    building_.cog_oid_.value = self.building_
    return building_
def _set_building(self, building_):
    self.building_.value = building_.cog_oid_

_building_ = property(
    _get_building, _set_building)

# REVERSE
@property
def _rev_event_(self):
    elt = self.db.table('collorg.event.event')
    elt._location_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

