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
import collorg.utils.globvars as glob

class Make_site(object):
    def __init__(self, controller):
        self.__ctrl = controller
        self.__db = controller.db
        self.__repo_path = self.__ctrl.repos_path
        self.pkg_path_1 = "%s/" % glob.cog_pkg_path(self.__db.name)
        self.__site_map_path = self.pkg_path_1.replace('/db/', '')
        #self.__make_site()

    def __make_site(self):
        print("Web site pages")
        os.stat(self.__site_map_path)
        cog_web_site_src = "%s/_cog_web_site/__src" % (self.__site_map_path)
        local_site = self.__db.table('collorg.web.site')
        local_site.url_.set_(self.__db._cog_params['url'])
        if not local_site.exists():
            local_site.insert()
        for (srcdirpath, dirnames, filenames) in os.walk(cog_web_site_src):
            src_file = ''
            nb_src_file = 0
            file_ = ''
            for file_ in filenames:
                if re.match('[^\.].*', file_):
                    if nb_src_file != 0:
                        print("ERROR! More than one file candidate in %s" % (
                            srcdirpath))
                        file_ = ''
                        break
                    src_file = file_
                if '.env' in filenames and '.data_type' in filenames:
                    print("ERROR! Environment and data_type are exclusive!")
                    break
                if file_ == '.env' or file_ == '.data_type':
                    continue
            environment = None
            if '.env' in filenames:
                environment = open("%s/.env"%(srcdirpath)).read().strip()
            data_type = None
            if '.data_type' in filenames:
                data_type = open("%s/.data_type"%(srcdirpath)).read().strip()
            if file_:
                page = local_site._rev_page_
                dirpath = srcdirpath.replace("/__src", "")
                path_info = re.sub('.*/__src', '', srcdirpath)
                if path_info == '':
                    path_info = '/'
                page.path_info_.set_intention(path_info)
                if not page.exists():
                    page.label_.set_intention(src_file)
                    page.cog_environment_.set_intention(environment)
                    page.data_type_.set_intention(data_type)
                    page.insert()
                else:
                    npage = page()
                    npage.cog_environment_.set_intention(environment)
                    npage.data_type_.set_intention(data_type)
                    npage.label_.set_intention(src_file)
                    page.update(npage)
                print("{}/{}".format(
                    path_info.encode('utf-8'), file_.encode('utf-8')))
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
