#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Displays the access
"""

import sys

from collorg.controller.controller import Controller

if __name__ == '__main__':
    ctrl = Controller()
    print(ctrl._d_anonymous_access)
    print(ctrl._d_visitor_access)
    
if False:#ÇA MARCHE PAS! LE SET_INTENTION SUR PVIEW!!!!
    action = None
    tv = ctrl._get_tasks_view()
    while action != "":
        action = raw_input("action: ")
        if action == '':
            sys.exit()
        fqtn = raw_input("fqtn: ")
        tv.name_.set_intention(action)
        tv.fqtn_.set_intention(fqtn)
        print(tv.select(just_return_sql = True))
        for elt in tv:
            print("%s" % (elt.task_name_))