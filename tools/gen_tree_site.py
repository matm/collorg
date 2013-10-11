#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os

if __name__ == '__main__':
    lines = open(sys.argv[1]).readlines()
    l_path = []
    for line in lines:
        l_items = line.rstrip().split('\t')
        item = l_items[-1]
        depth = len(l_items)
        while len(l_path) >= len(l_items) and len(l_path):
            l_path.pop()
        l_path.append(item)
        path = "collorg/_cog_web_site/__src/%s"%(
            "/".join(l_path)).replace(" ", "_").lower()
        file_name = "%s/=%s=" % (path, item.capitalize())
        os.makedirs(path)
        open(file_name,"w").write(item)
