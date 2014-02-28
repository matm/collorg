# DIRECT
def _get_data_type(self):
    data_type_ = self.db.table('collorg.core.data_type')
    data_type_.fqtn_.set_intention(self.data_type_)
    return data_type_
def _set_data_type(self, data_type_):
    self.data_type_.set_intention(data_type_.fqtn_)

_data_type_ = property(
    _get_data_type, _set_data_type)

# REVERSE
@property
def _rev_checked_val_(self):
    elt = self.db.table('collorg.core.checked_val')
    elt._field_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_translation_(self):
    elt = self.db.table('collorg.i18n.translation')
    elt._field_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_comment_(self):
    elt = self.db.table('collorg.communication.comment')
    elt._field_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

