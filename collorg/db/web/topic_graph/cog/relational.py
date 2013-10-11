# DIRECT
def _get_topic(self):
    topic_ = self.db.table('collorg.web.topic')
    topic_.cog_oid_.set_intention(self.topic_)
    return topic_
def _set_topic(self, topic_):
    self.topic_.set_intention(topic_.cog_oid_)

_topic_ = property(
    _get_topic, _set_topic)

def _get_parent(self):
    parent_ = self.db.table('collorg.core.oid_table')
    parent_.cog_oid_.set_intention(self.parent_)
    return parent_
def _set_parent(self, parent_):
    self.parent_.set_intention(parent_.cog_oid_)

_parent_ = property(
    _get_parent, _set_parent)

