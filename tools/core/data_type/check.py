#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

table = Controller().db.table

data_types = table('collorg.core.data_type')

for dt in data_types:
    try:
        table(dt.fqtn_.value)
    except Exception as err:
        print("{}: {}".format(dt.fqtn_, err))
