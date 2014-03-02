#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
attach an existing function to a task
"""

import sys
from collorg.controller.controller import Controller

if sys.version_info.major < 3:
    input = raw_input

if __name__ == '__main__':
    db = Controller().db
    f_long_name = sys.argv[1]
    function = db.table('collorg.actor.function')
    function.long_name_.value = f_long_name
    if function.count() != 1:
        sys.stderr.write("No such function (%s)\nAborting\n" % (f_long_name))
        sys.exit()
    task_name = sys.argv[2]
    task = db.table('collorg.application.task')
    task.name_.value = task_name
    if task.count() != 1:
        sys.stderr.write("No such task %s\nAborting\n" % (task_name))
        sys.exit()
    ok = input('ok [y/N]: ')
    if ok.upper() != 'Y':
        sys.stderr.write("exiting\n")
        sys.exit()
    atf = task._rev_a_task_function_
    atf._function_ = function
    if atf.count() == 0:
        print("+ task<->function: %s<->%s" % (
            task.name_, function.long_name_))
        atf.insert()
