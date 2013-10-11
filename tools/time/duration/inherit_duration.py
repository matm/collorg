#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller
import sys

db = Controller().db
table = db.table

alter_table = """
alter table {} add column cog_from timestamp(0);
alter table {} add column cog_to timestamp(0);
"""
alter_inh = """
alter table {} inherit "collorg.time".duration;
"""

if __name__ == '__main__':
    fqtn = sys.argv[1]
    obj = table(fqtn)
    if 'collorg.time.duration' in obj._cog_fqtn_inherits:
        sys.stderr.write('Already inherited!')
    sql_cmd = alter_table.format(obj.sql_fqtn, obj.sql_fqtn)
    if len(sys.argv) > 2:
        sql_cmd += alter_inh.format(obj.sql_fqtn)
    db.raw_sql(sql_cmd)
    db.commit()
