#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

if sys.version_info.major < 3:
    input = raw_input

db = Controller().db
oid_post = input('post oid: ')
post = db.get_elt_by_oid(oid_post)
print(post.cog_label())
oid_data = input('data oid: ')
data = db.get_elt_by_oid(oid_data)
print(data.cog_label())

ok = input('ok [o/N]')
if ok.upper() == 'O':
    apd = db.table('collorg.communication.blog.a_post_data')
    apd._post_ = post
    apd._data_ = data
    apd.insert()

