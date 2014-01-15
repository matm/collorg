#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

data = table(sys.argv[1])
for elt in data:
    elt._wipe_cache()
