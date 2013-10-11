# REVERSE
@property
def _rev_a_task_goal_(self):
    elt = self.db.table('collorg.activity.a_task_goal')
    elt._task_ = self
    return elt

@property
def _goal__s_(self):
    return self._rev_a_task_goal_._goal_

