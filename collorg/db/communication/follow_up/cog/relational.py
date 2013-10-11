# DIRECT
def _get_comment(self):
    comment_ = self.db.table('collorg.communication.comment')
    comment_.cog_oid_.set_intention(self.comment_)
    return comment_
def _set_comment(self, comment_):
    self.comment_.set_intention(comment_.cog_oid_)

_comment_ = property(
    _get_comment, _set_comment)

def _get_author(self):
    author_ = self.db.table('collorg.actor.user')
    author_.cog_oid_.set_intention(self.author_)
    return author_
def _set_author(self, author_):
    self.author_.set_intention(author_.cog_oid_)

_author_ = property(
    _get_author, _set_author)

