#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Test: associates the actions not in tasks to the task "Anonymous navigation"
to allow navigation.
"""

from collorg.controller.controller import Controller

if __name__ == '__main__':
    db = Controller().db
    for label, function in [
        ('Authenticated navigation','Authenticated user'),
        ('Anonymous navigation', 'Anonymous user')]:
        goal = db.table('collorg.application.goal')
        goal.name_.set_intention(label)
        if goal.count() == 0:
            goal.insert()
        task = db.table('collorg.application.task')
        task.name_.set_intention(label)
        if task.count() == 0:
            task.insert()
            # link anonymous navigation to anonymous role
            func = db.table('collorg.actor.function')
            func.name_.set_intention(function)
            atf = task._rev_a_task_function_
            atf._function_ = func
            atf.insert()
        atg = task._rev_a_task_goal_
        atg._goal_ = goal
        if atg.count() == 0:
            atg.insert()
    # link all the actions not in tasks to "anonymous navigation"
    for action in db.table('collorg.application.action'):
        if action._rev_a_action_task_._task_.count() == 0:
            rat = action._rev_a_action_task_
            rat._task_ = task
            rat.insert()
