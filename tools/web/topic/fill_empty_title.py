#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

topics = table("collorg.web.topic")
topics.title_.set_intention("")
for topic in topics:
    if not topic.cog_environment_.value:
        continue
    try:
        obj = db.get_elt_by_oid(topic.cog_environment_.value)
    except:
        topic.delete()
        continue
    nt = topic()
    nt.title_.set_intention(obj.cog_label())
    topic.update(nt)
