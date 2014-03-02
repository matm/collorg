# DIRECT
def _get_comment(self):
    comment_ = self.db.table('collorg.communication.comment')
    comment_.cog_oid_.value = self.comment_
    return comment_
def _set_comment(self, comment_):
    self.comment_.value = comment_.cog_oid_

_comment_ = property(
    _get_comment, _set_comment)

def _get_author(self):
    author_ = self.db.table('collorg.actor.user')
    author_.cog_oid_.value = self.author_
    return author_
def _set_author(self, author_):
    self.author_.value = author_.cog_oid_

_author_ = property(
    _get_author, _set_author)

