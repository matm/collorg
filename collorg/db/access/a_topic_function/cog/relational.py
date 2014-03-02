# DIRECT
def _get_topic(self):
    topic_ = self.db.table('collorg.web.topic')
    topic_.cog_oid_.value = self.topic_
    return topic_
def _set_topic(self, topic_):
    self.topic_.value = topic_.cog_oid_

_topic_ = property(
    _get_topic, _set_topic)

def _get_function(self):
    function_ = self.db.table('collorg.actor.function')
    function_.cog_oid_.value = self.function_
    return function_
def _set_function(self, function_):
    self.function_.value = function_.cog_oid_

_function_ = property(
    _get_function, _set_function)

