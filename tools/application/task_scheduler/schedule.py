#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

tasks = table('collorg.application.task').select()

i = 0
for task in tasks:
    print("{} {}".format(i, task.name_))
    i += 1
task_num = raw_input('Task to schedule? ')

print tasks[int(task_num)].name_

from_day  = raw_input("Begining date 'YYYY-MM-DD'? ")
from_hour  = raw_input("Begining hour 'HH:MM'? ")
to_day  = raw_input("End date 'YYYY-MM-DD'? ")
to_hour  = raw_input("End hour 'HH:MM'? ")

from_date = '{} {}:00'.format(from_day, from_hour)
to_date = '{} {}:00'.format(to_day, to_hour)

task = tasks[int(task_num)]
ts = task._rev_task_scheduler_
ts.cog_from_.set_intention(from_date)
ts.cog_to_.set_intention(to_date)
ts.insert()

nt = task()
nt.cog_from_.set_intention(from_date)
nt.cog_to_.set_intention(to_date)
task.update(nt)
