# DIRECT
def _get_rss(self):
    rss_ = self.db.table('collorg.web.rss')
    rss_.key_.set_intention(self.rss_)
    return rss_
def _set_rss(self, rss_):
    self.rss_.set_intention(rss_.key_)

_rss_ = property(
    _get_rss, _set_rss)

def _get_topic(self):
    topic_ = self.db.table('collorg.web.topic')
    topic_.cog_oid_.set_intention(self.topic_)
    return topic_
def _set_topic(self, topic_):
    self.topic_.set_intention(topic_.cog_oid_)

_topic_ = property(
    _get_topic, _set_topic)

