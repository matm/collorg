#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

db = Controller().db
table = db.table

data_types = table('collorg.core.data_type')

for dt in data_types:
    try:
        table(dt.fqtn_.value)
    except Exception as err:
        print("{}: {}".format(dt.fqtn_, err))
        ok = raw_input('Remove entry from database [N/y] ? ')
        if ok.upper() == 'Y':
            dt._rev_field_.delete()
            dt.delete()
            db.raw_sql('drop table {}'.format(
                    db._fqtn_2_sql_fqtn(dt.fqtn_.value)))

