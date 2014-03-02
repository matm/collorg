# DIRECT
def _get_topic(self):
    topic_ = self.db.table('collorg.web.topic')
    topic_.cog_oid_.value = self.topic_
    return topic_
def _set_topic(self, topic_):
    self.topic_.value = topic_.cog_oid_

_topic_ = property(
    _get_topic, _set_topic)

def _get_parent(self):
    parent_ = self.db.table('collorg.web.topic')
    parent_.cog_oid_.value = self.parent_
    return parent_
def _set_parent(self, parent_):
    self.parent_.value = parent_.cog_oid_

_parent_ = property(
    _get_parent, _set_parent)

