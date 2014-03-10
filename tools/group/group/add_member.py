#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

if sys.version_info.major < 3:
    input = raw_input

ctrl = Controller()
db = ctrl.db
table = db.table

groups = table('collorg.group.group')
groups.order_by(groups.name_)
for funct in groups:
    print(" - {}".format(funct.name_))
group_name = input("group name? ")
if not group_name.strip():
    sys.exit()
group = groups()
group.name_.value = group_name
group.get()
access = group._rev_access_
access.granted()
for user in access._user_:
    print(" - {}".format(user.pseudo_))
while True:
    last_name = input("Name? ")
    if not last_name.strip():
        sys.exit()
    users = table("collorg.actor.user")
    users.last_name_.value = last_name.strip(), 'ilike'
    for user in users:
        print(" - {} {} {}".format(
            user.cog_oid_, user.first_name_, user.last_name_))
    user_oid = input("User's OID? ")
    if not user_oid:
        continue
    user = db.get_elt_by_oid(user_oid)
    access._user_ = user
    access.write_.value = True
    access.insert()
