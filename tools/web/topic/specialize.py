#!/usr/bin/env python
#-*- coding: utf-8

import sys
from collorg.controller.controller import Controller

ctrl = Controller()
db = ctrl.db
table = db.table

topic = table('collorg.web.topic')
topic.path_info_.set_intention(sys.argv[1])
topic.get()
fqtn, action_name = sys.argv[2].rsplit('.', 1)
action = table('collorg.application.action')
action.data_type_.set_intention(fqtn)
action.name_.set_intention(action_name)
action.get()

n_topic = topic()
n_topic.data_type_.set_intention(fqtn)
n_topic._action_ = action

topic.update(n_topic)
