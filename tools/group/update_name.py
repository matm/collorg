#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

l_fqtn = ['organization.department', 'organization.team', 'collorg.actor.user']

db = Controller().db
groups = db.table('collorg.group.group')
for group in groups:
    data = group._data_.get()
    function = group._rev_a_group_role_._role_._function_
    if function.count() > 1:
        continue
    function.get()
    ng = group()
    if data.cog_fqtn_ in ['organization.department', 'organization.team']:
        ng.name_.value = '{} {}'.format(function.name_, data.acronym_)
    if data.cog_fqtn_ in ['collorg.actor.user']:
        ng.name_.value = "{} {}'s private group".format(
            data.first_name_, data.last_name_)
    group.update(ng)
