#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from datetime import datetime
from random import random
from collorg.controller.controller import Controller

path = sys.argv[0].rsplit('/', 1)[0]

ctrl = Controller()
table = ctrl.db.table
post_table = table('collorg.communication.blog.post')
topics = table('collorg.web.topic')
topics.site_.set_not_null()
topics_oids = []
for topic in topics:
    topics_oids.append(topic.cog_oid_.value)

print(int(random() * 3) + 1)

visibilities = ['private', 'protected', 'public']
users = []
for user in table('collorg.actor.user'):
    users.append(user)

texts = open("{}/lipsum.txt".format(path)).readlines()
titles = open("{}/lipsum_titles.txt".format(path)).readlines()

last = datetime.now()
for i in range(100000):
    if i and i % 1000 == 0:
        now = datetime.now()
        print(now - last)
        last = now
    idx_title = int(random() * 300)
    idx_text = int(random() * 300)
    post = post_table()
    user = users[int(random()*len(users))]
    ctrl.user = user
    print ctrl.user.pseudo_
    post.winsert(user=user.get(),
        data_oid=topics_oids[int(random()*len(topics_oids))],
        title_=titles[idx_title],
        text_=texts[idx_text],
        comment_=int(random() * 2) % 2,
        visibility_=visibilities[int(random() * 3)])

