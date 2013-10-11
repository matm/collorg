#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

if __name__ == '__main__':
    ctrl = Controller()
    db = ctrl.db
    task = db.table('collorg.application.task')
    if sys.version < '3':
        task_name = raw_input('task name: ')
    else:
        task_name = input('task name: ')
    task.name_.set_intention(task_name)
    actions = task._action__s_
    for action in actions:
        print("%s %s" % (action.name_.val, action.label_.val))
    goals = task._goal__s_
    for goal in goals:
        print(goal.name_.val)
