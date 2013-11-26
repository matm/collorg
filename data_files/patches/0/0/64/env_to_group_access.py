#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Pour tous les topics n'ayant pas de data_type et dont le champ cog_environment
est un groupe :
1)
  ajouter un accès group avec :
  * group_data = cog_environment
  * accessed_data = self
2) donner à cog_environement la valeur du cog_oid (cog_env == self)
"""

import sys
from collorg.controller.controller import Controller
table = Controller().db.table

groups = table('collorg.group.group')
units = table('collorg.organization.unit')
data_type = table('collorg.core.data_type')
topics = table('collorg.web.topic')
topics.data_type_.set_null()
topics.cog_environment_.set_intention(groups.cog_oid_ + units.cog_oid_)
topics.site_.set_not_null()

for topic in topics:
    print(topic.cog_label())
    group = groups()
    group.cog_oid_.set_intention(topic._cog_environment_.cog_oid_)
    if group.exists():
        group.grant_access(topic)
    ntopic = topic()
    ntopic.cog_environment_.set_intention(topic.cog_oid_.value)
    topic.update(ntopic)
