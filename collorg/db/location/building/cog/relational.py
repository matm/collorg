# DIRECT
def _get_address(self):
    address_ = self.db.table('collorg.location.address')
    address_.cog_oid_.value = self.address_
    return address_
def _set_address(self, address_):
    self.address_.value = address_.cog_oid_

_address_ = property(
    _get_address, _set_address)

def _get_site(self):
    site_ = self.db.table('collorg.location.site')
    site_.cog_oid_.value = self.site_
    return site_
def _set_site(self, site_):
    self.site_.value = site_.cog_oid_

_site_ = property(
    _get_site, _set_site)

# REVERSE
@property
def _rev_room_(self):
    elt = self.db.table('collorg.location.room')
    elt._building_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

