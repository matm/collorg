#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

if __name__ == '__main__':
    db = Controller().db
    function = db.table('collorg.actor.function')
    function.order_by(function.long_name_)
    for fctn in function:
        print(fctn.long_name_.val)
    if sys.version < '3':
        fctn_lng_name = raw_input("name: ")
    else:
        fctn_lng_name = input("name: ")
    the_function = function()
    the_function.long_name_.set_intention(fctn_lng_name)
    data = the_function._data_type_.get()()
    for dt in data:
        print("%s : %s" % (dt.cog_oid_.val, dt.cog_label()))
    data_oid = raw_input("oid data: ")
    data.cog_oid_.set_intention(data_oid)
    role = the_function._rev_role_
    user = db.table('collorg.actor.user')
    pseudo = raw_input('pseudo: ')
    user.pseudo_.set_intention(pseudo)
    access = user._rev_access_
    access._data_ = data
    if not access.is_granted():
        access = access.insert()
    access.granted()
    access = access.get()
    role._access_ = access
    role.insert()
