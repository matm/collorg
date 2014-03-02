# DIRECT
def _get_action(self):
    action_ = self.db.table('collorg.application.action')
    action_.cog_oid_.value = self.action_
    return action_
def _set_action(self, action_):
    self.action_.value = action_.cog_oid_

_action_ = property(
    _get_action, _set_action)

def _get_task(self):
    task_ = self.db.table('collorg.application.task')
    task_.cog_oid_.value = self.task_
    return task_
def _set_task(self, task_):
    self.task_.value = task_.cog_oid_

_task_ = property(
    _get_task, _set_task)

