# DIRECT
def _get_me(self):
    me_ = self.db.table('collorg.actor.user')
    me_.cog_oid_.set_intention(self.me_)
    return me_
def _set_me(self, me_):
    self.me_.set_intention(me_.cog_oid_)

_me_ = property(
    _get_me, _set_me)

def _get_my_relation(self):
    my_relation_ = self.db.table('collorg.actor.user')
    my_relation_.cog_oid_.set_intention(self.my_relation_)
    return my_relation_
def _set_my_relation(self, my_relation_):
    self.my_relation_.set_intention(my_relation_.cog_oid_)

_my_relation_ = property(
    _get_my_relation, _set_my_relation)

