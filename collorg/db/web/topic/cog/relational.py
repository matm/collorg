# DIRECT
def _get_data_type(self):
    data_type_ = self.db.table('collorg.core.data_type')
    data_type_.fqtn_.value = self.data_type_
    return data_type_
def _set_data_type(self, data_type_):
    self.data_type_.value = data_type_.fqtn_

_data_type_ = property(
    _get_data_type, _set_data_type)

def _get_post_type(self):
    post_type_ = self.db.table('collorg.core.data_type')
    post_type_.fqtn_.value = self.post_type_
    return post_type_
def _set_post_type(self, post_type_):
    self.post_type_.value = post_type_.fqtn_

_post_type_ = property(
    _get_post_type, _set_post_type)

def _get_action(self):
    action_ = self.db.table('collorg.application.action')
    action_.cog_oid_.value = self.action_
    return action_
def _set_action(self, action_):
    self.action_.value = action_.cog_oid_

_action_ = property(
    _get_action, _set_action)

def _get_author(self):
    author_ = self.db.table('collorg.actor.user')
    author_.cog_oid_.value = self.author_
    return author_
def _set_author(self, author_):
    self.author_.value = author_.cog_oid_

_author_ = property(
    _get_author, _set_author)

def _get_site(self):
    site_ = self.db.table('collorg.web.site')
    site_.cog_oid_.value = self.site_
    return site_
def _set_site(self, site_):
    self.site_.value = site_.cog_oid_

_site_ = property(
    _get_site, _set_site)

# REVERSE
@property
def _rev_a_rss_topic_(self):
    elt = self.db.table('collorg.web.a_rss_topic')
    elt._topic_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_wall_topic_(self):
    elt = self.db.table('collorg.web.wall')
    elt._topic_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_wall_parent_(self):
    elt = self.db.table('collorg.web.wall')
    elt._parent_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_a_topic_function_(self):
    elt = self.db.table('collorg.access.a_topic_function')
    elt._topic_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

