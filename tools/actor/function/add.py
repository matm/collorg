#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Add a new function to the database.
The arguments are:
    * name
    * long_name
    * data_type (fqtn)
    * optional: inst_group name
"""

from collorg.controller.controller import Controller
import sys

if __name__ == '__main__':
    db = Controller().db
    inst_group = None
    if len(sys.argv) == 5:
        ig_name = sys.argv[4]
        inst_group = db.table('collorg.actor.inst_group')
        inst_group.name_.set_intention(ig_name)
        if inst_group.count() == 0:
            sys.stderr.write("No such inst_group %s\nAborting\n" % (ig_name))
            sys.exit()
    name = sys.argv[1]
    long_name = sys.argv[2]
    fqtn = sys.argv[3]
    function = db.table('collorg.actor.function')
    function.long_name_.set_intention(long_name)
    if function.count():
        sys.stderr.write(
            "this function already exists (%s)\nAborting\n" % (long_name))
        sys.exit()
    ok = raw_input('ok [y/N]: ')
    if ok.upper() != 'Y':
        sys.stderr.write("exiting\n")
        sys.exit()
    function.name_.set_intention(name)
    function.fname_.set_intention(name)
    function.data_type_.set_intention(fqtn)
    function.insert()
    if inst_group is not None:
        fig = function._rev_a_function_inst_group_
        fig._inst_group_ = inst_group
        fig.insert()