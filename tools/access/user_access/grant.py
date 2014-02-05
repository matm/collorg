#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

usage = """usage: {} <accessed object oid> <user_oid> {{True}}

{}
"""

table = Controller().db.table
accessed_data = table('collorg.core.oid_table')
user = table('collorg.actor.user')

def grant_access(accessed_data, user, write):
    user_access = table('collorg.access.access')
    user_access._data_ = accessed_data
    user_access._user_ = user
    if write:
        user_access.write_.set_intention(write)
    if not user_access.exists():
        print("Grant access \n  for user: {}\n  to accessed object: {}".format(
            user.cog_label(), accessed_data.cog_label()))
        user_access.insert()
    else:
        print("Access already granted for {}".format(user.cog_label()))

try:
    try:
        assert len(sys.argv) in [3, 4]
    except:
        raise ValueError("")

    accessed_data.cog_oid_.set_intention(sys.argv[1])
    try:
        accessed_data = accessed_data.get()
    except:
        raise ValueError("Accessed object does not exist")
    user.cog_oid_.set_intention(sys.argv[2])
    try:
        user = user.get()
    except:
        raise ValueError("User does not exist")
    write = None
    if sys.argv[3] == 'True':
        write = True
    grant_access(accessed_data, user, write)
except Exception as err:
    if err:
        print(usage.format(sys.argv[0], err))
