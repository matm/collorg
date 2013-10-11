#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

import argparse
from collorg.controller.controller import Controller

help_ = """
dumps the content of a table.
formats are:
* json (Default)
* csv (NotImplemented)
* xml (NotImplemented)
"""


class Cmd():
    cmd_help = (help_)
    formats = ['json', 'csv', 'xml']
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.__parse_args()
        self.__dump()

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog dump")
        parser.add_argument(
            "-t", "--table_name", help = "restricts dump to a table",
            required = True)
        parser.add_argument(
            "-f", "--format", help = "restricts dump to a table")
        self.__args = parser.parse_args()

    def __dump(self):
        db = self.__ctrl.db
        table = db.table(self.__args.table_name)
        table.cog_light = True
        print("%s" % str([elt.raw() for elt in table]))
