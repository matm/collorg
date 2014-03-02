# DIRECT
def _get_data_oid(self):
    data_oid_ = self.db.table('collorg.core.oid_table')
    data_oid_.cog_oid_.value = self.data_oid_
    return data_oid_
def _set_data_oid(self, data_oid_):
    self.data_oid_.value = data_oid_.cog_oid_

_data_oid_ = property(
    _get_data_oid, _set_data_oid)

def _get_field(self):
    field_ = self.db.table('collorg.core.field')
    field_.fqfn_.value = self.field_
    return field_
def _set_field(self, field_):
    self.field_.value = field_.fqfn_

_field_ = property(
    _get_field, _set_field)

def _get_language(self):
    language_ = self.db.table('collorg.i18n.language')
    language_.cog_oid_.value = self.language_
    return language_
def _set_language(self, language_):
    self.language_.value = language_.cog_oid_

_language_ = property(
    _get_language, _set_language)

