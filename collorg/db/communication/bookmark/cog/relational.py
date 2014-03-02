# DIRECT
def _get_post(self):
    post_ = self.db.table('collorg.core.oid_table')
    post_.cog_oid_.value = self.post_
    return post_
def _set_post(self, post_):
    self.post_.value = post_.cog_oid_

_post_ = property(
    _get_post, _set_post)

def _get_user(self):
    user_ = self.db.table('collorg.actor.user')
    user_.cog_oid_.value = self.user_
    return user_
def _set_user(self, user_):
    self.user_.value = user_.cog_oid_

_user_ = property(
    _get_user, _set_user)

