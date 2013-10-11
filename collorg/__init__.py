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

__import__('pkg_resources').declare_namespace(__name__)
__doc__ = """
collaborative organization framework

Mainly used in a collorg directory as follows

from collorg.controller.controller import Controller
db = Controller().db
my_obj = db.table(<fully qualified table name>)
my_obj.do_some_stuff()
...

see cog command to manage a collorg repository
"""
