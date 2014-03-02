#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller

"""
give information on the elements with a cog_oid begining with sys.argv[1]
"""

if __name__ == '__main__':
    db = Controller().db
    ot = db.table('collorg.core.oid_table')
    ot.cog_oid_.value = '%s%%' % (sys.argv[1]), 'like'
    for elt in ot:
        print("%s: %s" % (elt.cog_oid_, elt.cog_fqtn_))
