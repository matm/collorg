#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

if sys.version_info.major < 3:
    input = raw_input

ctrl = Controller()
db = ctrl.db
table = db.table

functions = table('collorg.actor.function')
functions.order_by(functions.long_name_)
for funct in functions:
    print(" - {}".format(funct.long_name_))
function_long_name = input("function name? ")
if not function_long_name.strip():
    sys.exit()
function = functions()
function.long_name_.set_intention(function_long_name)
function.get()
access = function._rev_role_._access_
access.granted()
for user in access._user_:
    print(" - {}".format(user.pseudo_))
pseudo = input("pseudo? ")
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
