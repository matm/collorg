#!/usr/bin/python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

apd = table('collorg.communication.blog.a_post_data')
apd.order_.set_not_null()
topics = table('collorg.web.topic')
topics.cog_oid_.value = apd._data_.cog_oid_
for topic in topics:
    topic._wipe_cache()
    print("{}: {}".format(
            topic.title_.value or db.get_elt_by_oid(
                topic.cog_environment_.value).cog_label(),
            topic._rev_a_post_data_data_._post_.count()))
    apds = topic._rev_a_post_data_data_
    apds.order_by(apd.order_, apd.cog_creat_date_)
    nb_elts = apds.count()
    idx_apd = nb_elts - 1
    for apd in apds:
        napd = apd()
        napd.order_.value = idx_apd
        apd.update(napd)
        print(" {} {}".format(apd.order_, apd._post_.get().cog_label()))
        idx_apd -= 1
