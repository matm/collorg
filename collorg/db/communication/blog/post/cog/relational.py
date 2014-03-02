# DIRECT
def _get_author(self):
    author_ = self.db.table('collorg.actor.user')
    author_.cog_oid_.value = self.author_
    return author_
def _set_author(self, author_):
    self.author_.value = author_.cog_oid_

_author_ = property(
    _get_author, _set_author)

