#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Add a new institutinal group to the database.
The arguments are:
    * name
    * long_name
    * data_type (fqtn)
"""

from collorg.controller.controller import Controller
import sys

if __name__ == '__main__':
    db = Controller().db
    name = sys.argv[1]
    long_name = sys.argv[2]
    fqtn = sys.argv[3]
    inst_group = db.table('collorg.actor.inst_group')
    inst_group.name_.set_intention(name)
    if inst_group.count():
        sys.stderr.write(
            "this group already exists (%s)\nAborting\n" % (name))
        sys.exit()
    ok = raw_input('ok [y/N]: ')
    if ok.upper() != 'Y':
        sys.stderr.write("exiting\n")
        sys.exit()
    inst_group.long_name_.set_intention(long_name)
    inst_group.data_type_.set_intention(fqtn)
    inst_group.insert()
