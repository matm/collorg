# REVERSE
@property
def _rev_a_task_goal_(self):
    elt = self.db.table('collorg.activity.a_task_goal')
    elt._goal_ = self
    return elt

@property
def _task__s_(self):
    return self._rev_a_task_goal_._task_

