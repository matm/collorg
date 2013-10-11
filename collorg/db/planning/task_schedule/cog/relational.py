# DIRECT
def _get_schedule_oid(self):
    schedule_oid_ = self.db.table('collorg.core.oid_table')
    schedule_oid_.cog_oid_.set_intention(self.schedule_oid_)
    return schedule_oid_
def _set_schedule_oid(self, schedule_oid_):
    self.schedule_oid_.set_intention(schedule_oid_.cog_oid_)

_schedule_oid_ = property(
    _get_schedule_oid, _set_schedule_oid)

def _get_schedule_fqtn(self):
    schedule_fqtn_ = self.db.table('collorg.core.oid_table')
    schedule_fqtn_.cog_fqtn_.set_intention(self.schedule_fqtn_)
    return schedule_fqtn_
def _set_schedule_fqtn(self, schedule_fqtn_):
    self.schedule_fqtn_.set_intention(schedule_fqtn_.cog_fqtn_)

_schedule_fqtn_ = property(
    _get_schedule_fqtn, _set_schedule_fqtn)

def _get_task(self):
    task_ = self.db.table('collorg.planning.task')
    task_.cog_oid_.set_intention(self.task_)
    return task_
def _set_task(self, task_):
    self.task_.set_intention(task_.cog_oid_)

_task_ = property(
    _get_task, _set_task)

