# DIRECT
def _get_action(self):
    action_ = self.db.table('collorg.application.action')
    action_.cog_oid_.set_intention(self.action_)
    return action_
def _set_action(self, action_):
    self.action_.set_intention(action_.cog_oid_)

_action_ = property(
    _get_action, _set_action)

def _get_state(self):
    state_ = self.db.table('collorg.application.state')
    state_.cog_oid_.set_intention(self.state_)
    return state_
def _set_state(self, state_):
    self.state_.set_intention(state_.cog_oid_)

_state_ = property(
    _get_state, _set_state)

def _get_data_oid(self):
    data_oid_ = self.db.table('collorg.core.oid_table')
    data_oid_.cog_oid_.set_intention(self.data_oid_)
    return data_oid_
def _set_data_oid(self, data_oid_):
    self.data_oid_.set_intention(data_oid_.cog_oid_)

_data_oid_ = property(
    _get_data_oid, _set_data_oid)

def _get_user(self):
    user_ = self.db.table('collorg.actor.user')
    user_.cog_oid_.set_intention(self.user_)
    return user_
def _set_user(self, user_):
    self.user_.set_intention(user_.cog_oid_)

_user_ = property(
    _get_user, _set_user)

def _get_transition(self):
    transition_ = self.db.table('collorg.application.transition')
    transition_.cog_oid_.set_intention(self.transition_)
    return transition_
def _set_transition(self, transition_):
    self.transition_.set_intention(transition_.cog_oid_)

_transition_ = property(
    _get_transition, _set_transition)

