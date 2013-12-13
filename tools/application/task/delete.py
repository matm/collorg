#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Suppress a task and all actions attached to it.
"""

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

tasks = table('collorg.application.task')
if len(sys.argv) >= 2:
    fqtn = sys.argv[1]
    actions = table('collorg.application.action')
    actions.data_type_.set_intention(fqtn)
    tasks = actions._rev_a_action_task_._task_
if len(sys.argv) == 2:
    for task in tasks:
        print("{} {}".format(task.cog_oid_.value[0:8], task.name_))
    task_oid = raw_input('Task oid: ')
    task = tasks()
    task.cog_oid_.set_intention('{}%'.format(task_oid), 'like')
    task = task.get()
    print("\n{}\n".format(task.name_))
    print(' Actions:')
    actions = task.actions
    actions.order_by(actions.data_type_)
    for action in actions:
        print(" . {} {}.{}".format(
                action.cog_oid_.value[0:8], action.data_type_, action.name_))
    
    suppress = raw_input('Suppress [N/y]? ')
    if suppress.upper() != 'Y':
        print("Nothing suppressed.")
        sys.exit()
else:
    task_oid = sys.argv[2]
    task = tasks()
    task.cog_oid_.set_intention('{}%'.format(task_oid), 'like')
    task = task.get()
    
task.delete()
