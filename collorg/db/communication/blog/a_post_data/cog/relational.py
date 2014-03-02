# DIRECT
def _get_post(self):
    post_ = self.db.table('collorg.core.oid_table')
    post_.cog_oid_.value = self.post_
    return post_
def _set_post(self, post_):
    self.post_.value = post_.cog_oid_

_post_ = property(
    _get_post, _set_post)

def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.value = self.data_
    return data_
def _set_data(self, data_):
    self.data_.value = data_.cog_oid_

_data_ = property(
    _get_data, _set_data)

def _get_who(self):
    who_ = self.db.table('collorg.actor.user')
    who_.cog_oid_.value = self.who_
    return who_
def _set_who(self, who_):
    self.who_.value = who_.cog_oid_

_who_ = property(
    _get_who, _set_who)

