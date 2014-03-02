# DIRECT
def _get_group_data(self):
    group_data_ = self.db.table('collorg.core.oid_table')
    group_data_.cog_oid_.value = self.group_data_
    return group_data_
def _set_group_data(self, group_data_):
    self.group_data_.value = group_data_.cog_oid_

_group_data_ = property(
    _get_group_data, _set_group_data)

def _get_accessed_data(self):
    accessed_data_ = self.db.table('collorg.core.oid_table')
    accessed_data_.cog_oid_.value = self.accessed_data_
    return accessed_data_
def _set_accessed_data(self, accessed_data_):
    self.accessed_data_.value = accessed_data_.cog_oid_

_accessed_data_ = property(
    _get_accessed_data, _set_accessed_data)

