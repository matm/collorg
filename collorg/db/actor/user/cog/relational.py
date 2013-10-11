# DIRECT
def _get_ldap(self):
    ldap_ = self.db.table('collorg.auth.d_ldap')
    ldap_.cog_oid_.set_intention(self.ldap_)
    return ldap_
def _set_ldap(self, ldap_):
    self.ldap_.set_intention(ldap_.cog_oid_)

_ldap_ = property(
    _get_ldap, _set_ldap)

def _get_photo(self):
    photo_ = self.db.table('collorg.communication.file')
    photo_.cog_oid_.set_intention(self.photo_)
    return photo_
def _set_photo(self, photo_):
    self.photo_.set_intention(photo_.cog_oid_)

_photo_ = property(
    _get_photo, _set_photo)

# REVERSE
@property
def _rev_a_user_category_(self):
    elt = self.db.table('collorg.actor.a_user_category')
    elt._user_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_post_(self):
    elt = self.db.table('collorg.communication.blog.post')
    elt._author_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_log_(self):
    elt = self.db.table('collorg.application.log')
    elt._user_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_user_check_(self):
    elt = self.db.table('collorg.communication.user_check')
    elt._user_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_topic_(self):
    elt = self.db.table('collorg.web.topic')
    elt._author_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_access_(self):
    elt = self.db.table('collorg.access.access')
    elt._user_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_bookmark_(self):
    elt = self.db.table('collorg.communication.bookmark')
    elt._user_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_attachment_(self):
    elt = self.db.table('collorg.communication.attachment')
    elt._author_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_file_(self):
    elt = self.db.table('collorg.communication.file')
    elt._uploader_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_session_(self):
    elt = self.db.table('collorg.web.session')
    elt._user_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_follow_up_(self):
    elt = self.db.table('collorg.communication.follow_up')
    elt._author_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_relation_me_(self):
    elt = self.db.table('collorg.actor.relation')
    elt._me_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_relation_my_relation_(self):
    elt = self.db.table('collorg.actor.relation')
    elt._my_relation_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_comment_(self):
    elt = self.db.table('collorg.communication.comment')
    elt._author_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_a_post_data_(self):
    elt = self.db.table('collorg.communication.blog.a_post_data')
    elt._who_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

