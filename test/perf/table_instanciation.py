#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller
from random import randint
from datetime import datetime

ctrl = Controller()
table = ctrl.db.table

data_types = table('collorg.core.data_type').select()
nb_data = data_types.count()

for i in range(10000):
    data_type = data_types[randint(0, nb_data - 1)]
    begin = datetime.now()
    table(data_type.fqtn_.value)
    end = datetime.now()
    duration = (end - begin).total_seconds()
    if duration > 0.01:
        print("Instanciation {}: {}".format(data_type.fqtn_, duration))

    
