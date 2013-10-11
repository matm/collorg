# DIRECT
def _get_function(self):
    function_ = self.db.table('collorg.actor.function')
    function_.cog_oid_.set_intention(self.function_)
    return function_
def _set_function(self, function_):
    self.function_.set_intention(function_.cog_oid_)

_function_ = property(
    _get_function, _set_function)

def _get_inst_group(self):
    inst_group_ = self.db.table('collorg.actor.inst_group')
    inst_group_.cog_oid_.set_intention(self.inst_group_)
    return inst_group_
def _set_inst_group(self, inst_group_):
    self.inst_group_.set_intention(inst_group_.cog_oid_)

_inst_group_ = property(
    _get_inst_group, _set_inst_group)

