# DIRECT
def _get_action(self):
    action_ = self.db.table('collorg.application.action')
    action_.cog_oid_.set_intention(self.action_)
    return action_
def _set_action(self, action_):
    self.action_.set_intention(action_.cog_oid_)

_action_ = property(
    _get_action, _set_action)

def _get_start_state(self):
    start_state_ = self.db.table('collorg.application.state')
    start_state_.cog_oid_.set_intention(self.start_state_)
    return start_state_
def _set_start_state(self, start_state_):
    self.start_state_.set_intention(start_state_.cog_oid_)

_start_state_ = property(
    _get_start_state, _set_start_state)

def _get_end_state(self):
    end_state_ = self.db.table('collorg.application.state')
    end_state_.cog_oid_.set_intention(self.end_state_)
    return end_state_
def _set_end_state(self, end_state_):
    self.end_state_.set_intention(end_state_.cog_oid_)

_end_state_ = property(
    _get_end_state, _set_end_state)

# REVERSE
@property
def _rev_log_(self):
    elt = self.db.table('collorg.application.log')
    elt._transition_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

