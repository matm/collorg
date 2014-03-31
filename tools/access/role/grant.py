#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from datetime import datetime
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--function", dest="function",
                      help="function to which the role is attached (long name)")
    parser.add_option("-t", "--type", dest="data_type",
                      help="Type to which the function is attached (FQTN)")
    parser.add_option("-l", "--list_functions", dest="list_functions",
                      action="store_true",
                      help="list the available functions", default=True)
    (options, args) = parser.parse_args()
    function = table('collorg.actor.function')
    function.data_type_.value = options.data_type
    if options.function:
        function.long_name_.value = options.function
        function.get()
        datas = db.table(function.data_type_.value)
        for data in datas:
            print("{}: {}".format(data.cog_oid_, data.cog_label()))
        data_oid = raw_input('Data oid? ')
        if not data_oid.strip():
            sys.exit()
        data = db.get_elt_by_oid(data_oid)
        pseudo = raw_input('Pseudo? ')
        user = table('collorg.actor.user', pseudo_=pseudo)
        user.get()
        access = user._rev_access_
        access._data_ = data
        access.granted()
        if access.is_empty():
            access.insert()
        access = access.get()
        role = function._rev_role_
        role._access_ = access
        role.insert()
    else:
        for fct in function:
            print(fct.long_name_)
    if not options.function:
        parser.print_help()
