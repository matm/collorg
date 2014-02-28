#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
attach an existing function to an existing inst_group (collorg.actor.inst_group)
"""

import sys
from collorg.controller.controller import Controller

if sys.version_info.major < 3:
    input = raw_input

if __name__ == '__main__':
    db = Controller().db
    f_long_name = sys.argv[1]
    function = db.table('collorg.actor.function')
    function.long_name_.set_intention(f_long_name)
    if function.count() == 0:
        sys.stderr.write("No such function (%s)\nAborting\n" % (f_long_name))
        sys.exit()
    ig_name = sys.argv[2]
    inst_group = db.table('collorg.actor.inst_group')
    inst_group.name_.set_intention(ig_name)
    if inst_group.count() == 0:
        sys.stderr.write("No such inst_group %s\nAborting\n" % (ig_name))
        sys.exit()
    ok = input('ok [y/N]: ')
    if ok.upper() != 'Y':
        sys.stderr.write("exiting\n")
        sys.exit()
    fig = function._rev_a_function_inst_group_
    fig._inst_group_ = inst_group
    fig.insert()
