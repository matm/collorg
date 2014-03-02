#!/usr/bin/env python
#-*- coding: utf-8 -*-

### Copyright © 2011 Joël Maïzi <joel.maizi@lirmm.fr>
### This file is part of collorg

### collorg is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Walks the ./_cog_web_site/__src tree and generates the module corresponding
to each page found in the tree.
_cog_web_site/__src is the root (home page) of the site.
In each directory under the __src there is one and only one file
=<label>= where label is the label of the page.
For instance :
    __src/=Home page=
    __src/admin/=Site administration page=
    ...

Considering ./_cog_web_site/__src/<path_info>/<label>
This script generates the module ./cog_web_site/<path_info>/page.py
"""

import os
import sys
import re
from collorg.controller.controller import Controller
from collorg.templates.parser import Parser

def make_site(cog_web_site):
    return
    print(cog_web_site)
    cog_web_site_src = "%s/__src"%(cog_web_site)
    os.stat(cog_web_site)
    local_site = db.table('collorg.web.site')
    local_site.url_.set_(db._cog_params['url'])
    if local_site.count() == 0:
        local_site.insert()
    for (srcdirpath, dirnames, filenames) in os.walk(cog_web_site_src):
        src_file = ''
        nb_src_file = 0
        file_ = ''
        for file_ in filenames:
            if re.match('.*', file_):
                if nb_src_file != 0:
                    print("more than one file candidate in %s" % (srcdirpath))
                    file_ = ''
                    break
                src_file = file_
        if file_:
            page = db.table('collorg.web.page').join(local_site)
            dirpath=srcdirpath.replace("/__src", "")
            path_info = re.sub('.*/__src', '', srcdirpath)
            if path_info == '':
                path_info = '/'
            page.path_info_.value = path_info
            if page.count() == 0:
                page.label_.value = src_file
                page.insert()
            print(path_info, file_)
            try:
                os.lstat(dirpath)
            except:
                os.mkdir(dirpath)
                open("%s/__init__.py"%(dirpath),"w")
            mod = Parser().parse(
                "w3display",
                open("%s/%s"%(srcdirpath,src_file)).read(),
                "w3display")
            of = open("%s/w3display.py"%(dirpath),"w")
            of.write(mod)
            of.close()

if __name__ == '__main__':
    db = Controller().db
    base_dir = os.path.abspath(os.path.curdir)
    if db.name == 'collorg_db':
        cws = ["%s/collorg/_cog_web_site"%(base_dir)]
    else:
        cws = ["%s/collorg_apps/%s/collorg_app/%s/_cog_web_site"%(
            os.environ['HOME'],db_name,db_name)]
    for rep in cws:
        make_site(rep)
