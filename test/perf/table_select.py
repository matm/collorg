#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller
from random import randint
from datetime import datetime
from collections import OrderedDict

ctrl = Controller()
table = ctrl.db.table

data_types = table('collorg.core.data_type').select()

result = {}
durations = []
ratios = []
d_fqtns = {}

def init():
    for elt in table('collorg.core.oid_table'):
        fqtn = elt.cog_fqtn_.value
    oid = elt.cog_oid_.value
    if not fqtn in d_fqtns:
        d_fqtns[fqtn] = []
    d_fqtns[fqtn].append(oid)

def get_random_oid(fqtn):
    nb_oids = len(d_fqtns[fqtn])
    return d_fqtns[fqtn][randint(0, nb_oids - 1)]

for type_ in data_types:
    data_type = table(type_.fqtn_.value)
    begin = datetime.now()
    data = data_type.select()
    count = data_type.count()
    end = datetime.now()
    duration = (end - begin).total_seconds()
    ratio = count / (duration*10000)
    ratios.append(ratio)
    result[ratio] = (type_.fqtn_.value, count, duration)
    durations.append(duration)
ratios.sort()

for ratio in ratios:
    fqtn, count, duration = result[ratio]
    print("{}: {} {} {}".format(fqtn, ratio, count, duration))


