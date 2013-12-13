#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
List the tasks and the functions they are attached to
* a_action_task
* a_task_function
"""

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

tasks = table('collorg.application.task')
for task in tasks:
    print("{} {}".format(task.name_, task.cog_oid_.value[0:8]))
    print(' Functions:')
    functions = task.functions
    functions.order_by(functions.name_)
    for function in functions:
        print(" * {} {}".format(function.cog_oid_.value[0:8], function.name_))
    print(' Actions:')
    actions = task.actions
    actions.order_by(actions.data_type_)
    for action in actions:
        print(" . {} {}.{}".format(
                action.cog_oid_.value[0:8], action.data_type_, action.name_))
