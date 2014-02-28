#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller
import sys

if sys.version_info.major < 3:
    input = raw_input

def choose_label(elt, *args):
    if len(args):
        l_val = []
        for arg in args:
            l_val.append("{}".format(elt.__dict__[arg.pyname]))
        label = " ".join(l_val)
    else:
        label = elt.cog_label()
    return label

def choose(list_, *args):
    if len(list_) == 1:
        return list_.get()
    i = 1
    list_.order_by(*args)
    for elt in list_:
        if elt.fqtn == 'collorg.core.oid_table':
            elt = elt.get()
        print("{}- {}".format(i, choose_label(elt, *args)))
        i += 1
    print
    choice = input("choice [1-{}]: ".format(i - 1))
    if not choice:
        sys.exit()
    return list_[int(choice) - 1]

if __name__ == '__main__':
    table = Controller().db.table
    site = table('collorg.web.site')
    site = choose(site)
    print(site.cog_label())
    topic = site._rev_topic_
    topic = choose(topic, topic.path_info_)
    print(topic.cog_label())
    post = topic._rev_a_post_data_data_._post_
    post = choose(post)
