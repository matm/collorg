#!/usr/bin/env python

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

post = table('collorg.communication.blog.post')
post.cog_oid_.value = sys.argv[1]
post.get().wdelete()
