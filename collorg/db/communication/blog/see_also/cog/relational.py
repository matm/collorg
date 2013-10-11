# DIRECT
def _get_post(self):
    post_ = self.db.table('collorg.core.oid_table')
    post_.cog_oid_.set_intention(self.post_)
    return post_
def _set_post(self, post_):
    self.post_.set_intention(post_.cog_oid_)

_post_ = property(
    _get_post, _set_post)

def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.set_intention(self.data_)
    return data_
def _set_data(self, data_):
    self.data_.set_intention(data_.cog_oid_)

_data_ = property(
    _get_data, _set_data)

