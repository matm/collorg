#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

group = table('collorg.group.group')

data_type = raw_input('Data type? ')
datas = table(data_type)
for data in datas:
    print(" - {} {}".format(data.cog_oid_, data.cog_label()))
data_oid = raw_input("Data oid? ")
data = db.get_elt_by_oid(data_oid)
owner_s_name = raw_input("Owner's name? ")
users = table('collorg.actor.user')
users.last_name_.set_intention(owner_s_name, 'ilike')
users.order_by(users.last_name_, users.first_name_)
for user in users:
    print(" - {} {} {}".format(user.cog_oid_, user.first_name_, user.last_name_))
owner_oid = raw_input("Owner's oid? ")
owner = db.get_elt_by_oid(owner_oid)

group_name = raw_input("Group name? ")
group_name = group_name.strip()
if not group_name:
    sys.exit()

group.name_.set_intention(group_name)
group._data_ = data
group.insert(user=owner)