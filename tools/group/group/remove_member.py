#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

groups = table('collorg.group.group')
groups.order_by(groups.name_)
for funct in groups:
    print(" - {}".format(funct.name_))
group_name = raw_input("group name? ")
if not group_name.strip():
    sys.exit()
group = groups()
group.name_.set_intention(group_name)
group.get()
access = group._rev_access_
access.granted()
for user in access._user_:
    print(" - {}".format(user.pseudo_))
pseudo = raw_input("pseudo? ")
if not pseudo.strip():
    sys.exit()
user = table("collorg.actor.user")
user.pseudo_.set_intention(pseudo.strip())
user.get()
access._user_ = user
for role in access._rev_role_:
    role.delete()
for acc in access:
    acc.delete()