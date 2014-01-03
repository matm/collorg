#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

table = Controller().db.table

lf = table('collorg.core.view.lost_found')
lf.clean()
