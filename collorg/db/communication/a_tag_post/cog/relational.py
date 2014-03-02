# DIRECT
def _get_data_type(self):
    data_type_ = self.db.table('collorg.core.data_type')
    data_type_.fqtn_.value = self.data_type_
    return data_type_
def _set_data_type(self, data_type_):
    self.data_type_.value = data_type_.fqtn_

_data_type_ = property(
    _get_data_type, _set_data_type)

def _get_post(self):
    post_ = self.db.table('collorg.core.oid_table')
    post_.cog_oid_.value = self.post_
    return post_
def _set_post(self, post_):
    self.post_.value = post_.cog_oid_

_post_ = property(
    _get_post, _set_post)

def _get_tag(self):
    tag_ = self.db.table('collorg.communication.tag')
    tag_.tag_.value = self.tag_
    return tag_
def _set_tag(self, tag_):
    self.tag_.value = tag_.tag_

_tag_ = property(
    _get_tag, _set_tag)

