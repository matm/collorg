#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

db = Controller().db
oid_post = raw_input('post oid: ')
post = db.get_elt_by_oid(oid_post)
print(post.cog_label())
oid_data = raw_input('data oid: ')
data = db.get_elt_by_oid(oid_data)
print(data.cog_label())

ok = raw_input('ok [o/N]')
if ok.upper() == 'O':
    apd = db.table('collorg.communication.blog.a_post_data')
    apd._post_ = post
    apd._data_ = data
    apd.insert()

