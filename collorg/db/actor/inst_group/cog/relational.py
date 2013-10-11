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
def _rev_a_function_inst_group_(self):
    elt = self.db.table('collorg.actor.a_function_inst_group')
    elt._inst_group_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

