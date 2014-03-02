# DIRECT
def _get_function(self):
    function_ = self.db.table('collorg.actor.function')
    function_.cog_oid_.value = self.function_
    return function_
def _set_function(self, function_):
    self.function_.value = function_.cog_oid_

_function_ = property(
    _get_function, _set_function)

def _get_category(self):
    category_ = self.db.table('collorg.actor.category')
    category_.cog_oid_.value = self.category_
    return category_
def _set_category(self, category_):
    self.category_.value = category_.cog_oid_

_category_ = property(
    _get_category, _set_category)

