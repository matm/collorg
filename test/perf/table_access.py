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
    print("ready")

def get_random_oid(fqtn):
    oids = d_fqtns[fqtn]
    nb_oids = len(oids)
    return oids[randint(0, nb_oids - 1)]

init()
for data_type in data_types:
    fqtn = data_type.fqtn_.value
    if not fqtn in d_fqtns:
        continue
    if fqtn in [
        'collorg.communication.a_tag_post', 'collorg.communication.tag']:
        continue
    try:
        data = table(fqtn)
    except:
        continue
    count = data.count()
    data.cog_oid_.value = get_random_oid(fqtn)
    begin = datetime.now()
    data.get()
    end = datetime.now()
    duration = (end - begin).total_seconds()
    ratio = count / (duration*10000)
    ratios.append(ratio)
    result[ratio] = (fqtn, count, duration)
ratios.sort()

for ratio in ratios:
    fqtn, count, duration = result[ratio]
    print("{}: {} {} {}".format(fqtn, ratio, count, duration))


