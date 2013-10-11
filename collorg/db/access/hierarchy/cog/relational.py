# DIRECT
def _get_parent(self):
    parent_ = self.db.table('collorg.core.oid_table')
    parent_.cog_oid_.set_intention(self.parent_)
    return parent_
def _set_parent(self, parent_):
    self.parent_.set_intention(parent_.cog_oid_)

_parent_ = property(
    _get_parent, _set_parent)

def _get_child(self):
    child_ = self.db.table('collorg.core.oid_table')
    child_.cog_oid_.set_intention(self.child_)
    return child_
def _set_child(self, child_):
    self.child_.set_intention(child_.cog_oid_)

_child_ = property(
    _get_child, _set_child)

