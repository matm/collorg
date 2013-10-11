#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

ctrl = Controller()
table = ctrl.db.table

users = table('collorg.actor.user')
for user in users:
    topics = table('collorg.web.topic')
    topics._environment_ = user
    for topic in topics:
        print("{} {}".format(user.pseudo_, topic.cog_oid_))
        user.grant_access(topic)
