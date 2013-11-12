#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import urllib
import json
import pprint
from random import randint
from datetime import datetime

from collorg.controller.controller import Controller

ctrl = Controller()
table = ctrl.db.table

data_types = table('collorg.core.data_type').select()

oids = []

def init():
    for elt in table('collorg.communication.blog.post'):
        oid = elt.cog_oid_.value
        oids.append(oid)
    print("ready")

def get_random_oid():
    nb_oids = len(oids)
    return oids[randint(0, nb_oids - 1)]

pp = pprint.PrettyPrinter(indent=4)
init()
for i in range(int(sys.argv[2])):
    oid = get_random_oid()
    begin = datetime.now()
    encoded_args = urllib.urlencode({'cog_ajax':'true'})
    res = urllib.urlopen("{}/{}".format(
        sys.argv[1], get_random_oid()), encoded_args).read()
    end = datetime.now()
    print(json.loads(res)['null']['content'])
    print("{} {}".format(oid, (end - begin).total_seconds()))

