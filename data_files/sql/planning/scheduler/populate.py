#!/usr/bin/env python
#-*- coding: utf-8

from collorg.controller.controller import Controller

week_days = ((0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
    (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'))
months = ((1,'January'), (2,'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'))

def year_week():
    for num in range(52):
        yw = db.table("collorg.planning.scheduler.year_week")
        yw.num_.set_intention(num + 1)
        if yw.count() == 0:
            yw.insert()

def month_day():
    for num in range(31):
        md = db.table("collorg.planning.scheduler.month_day")
        md.num_.set_intention(num + 1)
        if md.count() == 0:
            md.insert()

def month_week_day():
    for elt in (
        ("collorg.planning.scheduler.month", months),
        ("collorg.planning.scheduler.week_day", week_days)):
        fqtn = elt[0]
        data = elt[1]
        for num, name in data:
            table = db.table(fqtn)
            table.num_.set_intention(num)
            table.name_.set_intention(name)
            if table.count() == 0:
                table.insert()

if __name__ == '__main__':
    db = Controller().db
    month_week_day()
    month_day()
    year_week()