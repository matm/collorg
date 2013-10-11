# DIRECT
def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.set_intention(self.data_)
    return data_
def _set_data(self, data_):
    self.data_.set_intention(data_.cog_oid_)

_data_ = property(
    _get_data, _set_data)

def _get_task(self):
    task_ = self.db.table('collorg.application.task')
    task_.cog_oid_.set_intention(self.task_)
    return task_
def _set_task(self, task_):
    self.task_.set_intention(task_.cog_oid_)

_task_ = property(
    _get_task, _set_task)

def _get_year(self):
    year_ = self.db.table('collorg.time.year')
    year_.num_.set_intention(self.year_)
    return year_
def _set_year(self, year_):
    self.year_.set_intention(year_.num_)

_year_ = property(
    _get_year, _set_year)

