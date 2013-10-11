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

import inspect
import os
import sys
from creole import creole2html
if sys.version >= '3':
    unicode = str

# src_file_name
template_do_not_edit = """#-*- coding: utf-8 -*-
##
##
## Do not edit this code!
## It has been generated from the source file:
## %s
##
"""

template_import = """
from collorg.templates.template import _cog_template
from collorg.templates.template import _format
from collorg.templates.document_type.html import Html
"""

# self.__template_name, self.__template_name
template_def = """
def %s( self, cog_did = '', **kwargs):
    charset = self._cog_controller._charset
    if not self._cog_controller.check(self, '%s'):
        return ""
    html = Html(self)
    cog_tmpl_out = {}
"""

# PRAGMA
template_pragma = """
    __PRAGMA = {{s}
"""

# self.__out_var (defined in parser)
template_out_var = """
    %s = "" # init of the template output var
"""

# assert self.__out_var == self.default_out_var
# "\n".join(["    %s" % (line) for line in template_code ])
template_code_lines = """
%s
"""

# self.__out_var, self.default_out_var
template_format = """
    if 'format' in __PRAGMA.keys():
        %s = _format(PRAGMA['format'], %s, charset)
"""

# self.default_out_var
template_cog_tmpl_out = """
    cog_tmpl_out[cog_target] = %s
    return cog_tmpl_out
"""

def _format(format_, text, charset):
    known_formats = ['wiki']
    if format_ not in known_formats:
        return "Unknown format:\n%s" % (text)
    if format_ == 'wiki':
        return creole2html(unicode(text, charset)).encode(charset)

