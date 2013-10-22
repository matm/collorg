#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

db = Controller().db
apd = db.table('collorg.communication.blog.a_post_data')
apd.order_by(apd.data_)
data = None
for elt in apd:
    if elt.data_.value != data:
        data = elt.data_.value
        i = 0
    nelt = elt()
    nelt.order_.set_intention(i)
    elt.update(nelt)
    i += 1

