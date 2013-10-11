# DIRECT
def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.set_intention(self.data_)
    return data_
def _set_data(self, data_):
    self.data_.set_intention(data_.cog_oid_)

_data_ = property(
    _get_data, _set_data)

def _get_tag(self):
    tag_ = self.db.table('collorg.communication.tag')
    tag_.tag_.set_intention(self.tag_)
    return tag_
def _set_tag(self, tag_):
    self.tag_.set_intention(tag_.tag_)

_tag_ = property(
    _get_tag, _set_tag)

