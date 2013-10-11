#!/usr/bin/env python

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

post = table('collorg.communication.blog.post')
post.cog_oid_.set_intention(sys.argv[1])
post = post.get()
data = table('collorg.core.oid_table')
data.cog_oid_.set_intention(sys.argv[2])
data = data.get()
apd = table('collorg.communication.blog.a_post_data')
apd._post_ = post
apd._data_ = data
if not apd.exists():
    apd.insert()
