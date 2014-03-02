#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

if sys.version_info.major < 3:
    input = raw_input

if __name__ == '__main__':
    db = Controller().db
    function = db.table('collorg.actor.function')
    function.order_by(function.long_name_)
    for fctn in function:
        print(fctn.long_name_)
    fctn_lng_name = input("name: ")
    the_function = function()
    the_function.long_name_.set_intention(fctn_lng_name)
    data = the_function._data_type_.get()()
    for dt in data:
        print("%s : %s" % (dt.cog_oid_, dt.cog_label()))
    data_oid = input("oid data: ")
    data.cog_oid_.set_intention(data_oid)
    role = the_function._rev_role_
    user = db.table('collorg.actor.user')
    pseudo = input('pseudo: ')
    user.pseudo_.set_intention(pseudo)
    access = user._rev_access_
    access._data_ = data
    access.granted()
    if not access.is_granted():
        access = access.insert()
    access = access.get()
    role._function_ = the_function
    role._access_ = access
    role.insert()
