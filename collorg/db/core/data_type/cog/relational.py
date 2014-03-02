# DIRECT
def _get_namespace(self):
    namespace_ = self.db.table('collorg.core.namespace')
    namespace_.cog_oid_.value = self.namespace_
    return namespace_
def _set_namespace(self, namespace_):
    self.namespace_.value = namespace_.cog_oid_

_namespace_ = property(
    _get_namespace, _set_namespace)

# REVERSE
@property
def _rev_action_(self):
    elt = self.db.table('collorg.application.action')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_topic_data_type_(self):
    elt = self.db.table('collorg.web.topic')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_topic_post_type_(self):
    elt = self.db.table('collorg.web.topic')
    elt._post_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_field_(self):
    elt = self.db.table('collorg.core.field')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_a_tag_post_(self):
    elt = self.db.table('collorg.communication.a_tag_post')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_function_(self):
    elt = self.db.table('collorg.actor.function')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_state_(self):
    elt = self.db.table('collorg.application.state')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

@property
def _rev_inst_group_(self):
    elt = self.db.table('collorg.actor.inst_group')
    elt._data_type_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__:
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt

