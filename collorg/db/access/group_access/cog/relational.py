# DIRECT
def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.set_intention(self.data_)
    return data_
def _set_data(self, data_):
    self.data_.set_intention(data_.cog_oid_)

_data_ = property(
    _get_data, _set_data)

def _get_group(self):
    group_ = self.db.table('collorg.group.group')
    group_.cog_oid_.set_intention(self.group_)
    return group_
def _set_group(self, group_):
    self.group_.set_intention(group_.cog_oid_)

_group_ = property(
    _get_group, _set_group)

