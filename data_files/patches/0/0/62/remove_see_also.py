#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

ctrl = Controller()
table = ctrl.db.table

a_post_data = table('collorg.communication.blog.a_post_data')

try:
    see_also = table('collorg.communication.blog.see_also')
    for sa in see_also:
        apd = a_post_data()
        apd.post_.value = sa.post_.value
        apd.data_.value = sa.data_.value
        apd.see_also_.value = True
        apd.insert()
        sa.delete()

    graph_topic = table('collorg.web.topic_graph')

    for gt in graph_topic:
        apd = a_post_data()
        apd.post_.value = gt.topic_.value
        apd.data_.value = gt.parent_.value
        if not apd.exists():
            apd.see_also_.value = False
            apd.insert()
        gt.delete()
except:
    pass

apd = a_post_data()
apd.order_by(apd.data_, apd.cog_creat_date_)
this = None
for elt in apd:
    if this != elt.data_.value:
        order = 0
        this = elt.data_.value
    napd = apd()
    napd.order_.value = order
    elt.update(napd)
    order += 1
