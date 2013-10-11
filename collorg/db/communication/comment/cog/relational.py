# DIRECT
def _get_data(self):
    data_ = self.db.table('collorg.core.oid_table')
    data_.cog_oid_.set_intention(self.data_)
    return data_
def _set_data(self, data_):
    self.data_.set_intention(data_.cog_oid_)

_data_ = property(
    _get_data, _set_data)

def _get_field(self):
    field_ = self.db.table('collorg.core.field')
    field_.fqfn_.set_intention(self.field_)
    return field_
def _set_field(self, field_):
    self.field_.set_intention(field_.fqfn_)

_field_ = property(
    _get_field, _set_field)

def _get_author(self):
    author_ = self.db.table('collorg.actor.user')
    author_.cog_oid_.set_intention(self.author_)
    return author_
def _set_author(self, author_):
    self.author_.set_intention(author_.cog_oid_)

_author_ = property(
    _get_author, _set_author)

# REVERSE
@property
def _rev_follow_up_(self):
    elt = self.db.table('collorg.communication.follow_up')
    elt._comment_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

