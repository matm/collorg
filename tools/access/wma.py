#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Tags write, moderate, admin according to a csv file
method_name, data_type, write, moderate, admin
"""

from collorg.controller.controller import Controller
import sys

if __name__ == '__main__':
    db = Controller().db
    tags_file = sys.argv[1]
    for line in open(tags_file).readlines():
        name, data_type, tags = line.split(';', 3)
        tags = tags.strip().split(';')
        action = db.table('collorg.application.action')
        action.name_.set_intention(name)
        action.data_type_.set_intention(data_type)
        naction = db.table('collorg.application.action')
        l_rights = [naction.write_, naction.moderate_, naction.admin_]
        idx = 0
        update = False
        for tag in tags:
            tag.strip()
            assert tag in ('t', 'f', '')
            if tag:
                update = True
                l_rights[idx].set_intention(tag)
            idx += 1
        if update:
            action.update(naction)
