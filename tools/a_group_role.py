#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller
import sys

if __name__ == '__main__':
    ctrl = Controller()
    db = ctrl.db
    roles = db.table('collorg.actor.role')
    roles.order_by(roles.tmp_name_)
    for role in roles:
        if role._group__s_.count() == 0:
            print(role.tmp_name_.val)
            groups = db.table('collorg.group.group')
            groups._data_ = role._data_
            groups.order_by(groups.name_)
            for group in groups:
                print(group.name_.val)
            gr_name = raw_input('group : ')
            if not gr_name:
                continue
            group = group(name_ = gr_name).get()
            agr = group._rev_a_group_role_
            agr._role_ = role
            agr.insert(role=role, group=group)
