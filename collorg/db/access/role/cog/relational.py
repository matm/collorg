# DIRECT
def _get_function(self):
    function_ = self.db.table('collorg.actor.function')
    function_.cog_oid_.value = self.function_
    return function_
def _set_function(self, function_):
    self.function_.value = function_.cog_oid_

_function_ = property(
    _get_function, _set_function)

def _get_access(self):
    access_ = self.db.table('collorg.access.access')
    access_.cog_oid_.value = self.access_
    return access_
def _set_access(self, access_):
    self.access_.value = access_.cog_oid_

_access_ = property(
    _get_access, _set_access)

