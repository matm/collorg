#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from datetime import datetime
from collorg.controller.controller import Controller

"""
Equivalent to tools/actor/function/revoke
"""

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
        roles = function._rev_role_
        roles.granted()
        for role in roles:
            access = role._access_
            user = access._user_.get()
            data = access._data_.get()
            print("{}: {}".format(role.cog_oid_, user.pseudo_))
        role_oid = raw_input('Role oid? ')
        if not role_oid.strip():
            sys.exit()
        role = roles()
        role.cog_oid_.value = role_oid
        role.get()
        access = role._access_.get()
        role.revoke(no_access=True, no_function=True)
    else:
        for fct in function:
            print(fct.long_name_)
    if not options.function:
        parser.print_help()
