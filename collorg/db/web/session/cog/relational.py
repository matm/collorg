# DIRECT
def _get_user(self):
    user_ = self.db.table('collorg.actor.user')
    user_.cog_oid_.value = self.user_
    return user_
def _set_user(self, user_):
    self.user_.value = user_.cog_oid_

_user_ = property(
    _get_user, _set_user)

