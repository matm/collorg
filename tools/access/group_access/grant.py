#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

usage = """usage: {} <accessed object oid> <group data oid>

{}
"""

table = Controller().db.table
accessed_data = table('collorg.core.oid_table')
group_data = table('collorg.core.oid_table')

def grant_access(accessed_data, group_data):
    print("Grant access \n  for group data: {}\n  to accessed object: {}".format(
        group_data.cog_label(), accessed_data.cog_label()))
    group_access = table('collorg.access.group_access')
    group_access._accessed_data_ = accessed_data
    group_access._group_data_ = group_data
    if group_access.is_empty():
        group_access.insert()

try:
    try:
        assert len(sys.argv) == 3
    except:
        raise ValueError("")

    accessed_data.cog_oid_.value = sys.argv[1]
    try:
        accessed_data = accessed_data.get()
    except:
        raise ValueError("Accessed object does not exist")
    group_data.cog_oid_.value = sys.argv[2]
    try:
        group_data = group_data.get()
    except:
        raise ValueError("Group data does not exist")
    grant_access(accessed_data, group_data)
except Exception as err:
    if err:
        print(usage.format(sys.argv[0], err))
