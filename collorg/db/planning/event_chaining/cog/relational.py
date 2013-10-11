# DIRECT
def _get_event(self):
    event_ = self.db.table('collorg.planning.event')
    event_.cog_oid_.set_intention(self.event_)
    return event_
def _set_event(self, event_):
    self.event_.set_intention(event_.cog_oid_)

_event_ = property(
    _get_event, _set_event)

def _get_next_event(self):
    next_event_ = self.db.table('collorg.planning.event')
    next_event_.cog_oid_.set_intention(self.next_event_)
    return next_event_
def _set_next_event(self, next_event_):
    self.next_event_.set_intention(next_event_.cog_oid_)

_next_event_ = property(
    _get_next_event, _set_next_event)

