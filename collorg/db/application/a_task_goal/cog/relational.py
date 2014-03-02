# DIRECT
def _get_task(self):
    task_ = self.db.table('collorg.application.task')
    task_.cog_oid_.value = self.task_
    return task_
def _set_task(self, task_):
    self.task_.value = task_.cog_oid_

_task_ = property(
    _get_task, _set_task)

def _get_goal(self):
    goal_ = self.db.table('collorg.application.goal')
    goal_.cog_oid_.value = self.goal_
    return goal_
def _set_goal(self, goal_):
    self.goal_.value = goal_.cog_oid_

_goal_ = property(
    _get_goal, _set_goal)

