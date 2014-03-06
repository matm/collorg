#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

ctrl = Controller()
table = ctrl.db.table

posts = table('collorg.communication.blog.post')
posts.cog_fqtn = 'collorg.communication.blog.post'
for post in posts:
    author = post._author_
    if not author.is_empty():
        author = author.get()
    else:
        continue
    accesses = post._rev_access_
    accesses.granted()
    for access in accesses:
        user = access._user_.get()
        if user.cog_oid_.value != author.cog_oid_.value:
            print("{} is not {}".format(user.pseudo_, author.pseudo_))
            naccess = access()
            naccess.write_.value = False
            access.update(naccess)
