# DIRECT
def _get_user(self):
    user_ = self.db.table('collorg.actor.user')
    user_.cog_oid_.set_intention(self.user_)
    return user_
def _set_user(self, user_):
    self.user_.set_intention(user_.cog_oid_)

_user_ = property(
    _get_user, _set_user)

def _get_category(self):
    category_ = self.db.table('collorg.actor.category')
    category_.cog_oid_.set_intention(self.category_)
    return category_
def _set_category(self, category_):
    self.category_.set_intention(category_.cog_oid_)

_category_ = property(
    _get_category, _set_category)

