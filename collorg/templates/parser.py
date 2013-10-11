#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Copyright © 2006-2011 Joël Maïzi <joel@collorg.org>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys
import re
#from Tracer import Tracer

do_not_edit_msg = (
    '##\n'
    '## Do not edit this code!\n'
    '## It has been generated from the source file:\n'
    '## \'%s\'.\n'
    '##\n' )

class Parser( object ):
    #__metaclass__ = Tracer
    """
    Pour l'instant très sommaire:
    * # >>>: marque d'indentation et de début de code python
    * # +++: marque la mise en place d'une variable de stockage
    * # ---: marque d'indentation et, le cas échéant, de fin de code python
    * {{...}}: code python embarqué dans une ligne
    * {#: en début de ligne, marque de début de commentaire, jusqu'à la ligne #}
    * #}: en début de ligne, marque de fin de commentaire multi-lignes.
    * #PRAGMA: directives pour le parser.
    """
    pragma = re.compile( r'^#PRAGMA\s.*' )
    in_code_mark = r'\s*# >>>'
    out_code_mark = r'\s*# ---'
    new_var_mark = r'\s*# \+\+\+'
    indent_regex = r'(%s|%s|%s)\s*([_a-zA-Z]*[_a-zA-Z0-9]*)' % (
            in_code_mark, out_code_mark, new_var_mark)
    comment_begin_mark = "{#"
    comment_end_mark = "#}"
    code_begin_inline_mark = "{%"
    code_end_inline_mark = "%}"
    inline_code = re.compile( '{%[^%][^}]*%}')
    default_out_var = '__cog_tmpl_out'

    def __init__( self, out_var = None, charset = 'utf-8'):
        self.__charset = charset
        self.__pragma = []
        self.__template_lines = []
        self.__in_code = False
        self.__in_comment = False
        self.__indentation = ""
        self.__strip = False
        self.__out_var = [self.default_out_var]

    @property
    def out_var(self):
        return self.__out_var[-1]

    def __escape_line( self, line ):
        line = line.replace('\\', '\\\\')
        line = line.replace('"', '\\"')
        return line

    def __pythonized_line(self, line, _code = False):
        cr = '\\n'
        if self.__strip:
            cr = ''
        if not _code:
            line = '"{}{}"'.format(self.__escape_line(line), cr)
            line = "{}.append({})".format(self.out_var, line)
        return line

    def __prepare_inline_code(self, line):
        cr = '\\n'
        if self.__strip:
            cr = ''
        l_l_elt = [elt.replace('{', '{{').replace('}', '}}') for elt in
            re.split(self.inline_code, self.__escape_line(line))]
        left_part = "{}".join(l_l_elt)
        left_part = '"""{}{}"""'.format(left_part, cr)
        right_part = ", ".join(
            [ i[2:-2] for i in re.findall(self.inline_code, line) ])
        return "{}.append({}.format({}))".format(
            self.out_var, left_part, right_part)

    def __pythonized_code_line(self, line):
        """
        la mal nommée. génère la ligne de code python en tenant compte de
        l''indentation.
        """
        if self.__strip:
            line = line.strip()
        if re.findall(self.inline_code, line):
            # si on a du code embarqué dans la ligne
            return self.__pythonized_line(
                self.__prepare_inline_code(line), _code = True)
        else:
            return self.__pythonized_line(line)

    def __gen_code(self, template_src_file_name = None):
        """
        la template a été "splitée" et se trouve dans self.__template_lines
        """
        template_code = []
        idx_line = 0
        for line in self.__template_lines:
            idx_line += 1
            if re.match(self.pragma, line):
                self.__pragma.append(line[8:])
                #!! re to match "strip" or 'strip' in pragma
                if line[8:].find( "'strip':" ) != -1:
                    strip = line[8:].replace( "'strip':", '' ).strip()
                    assert strip == 'True' or strip == 'False'
                    self.__strip = False
                    if strip == 'True':
                        self.__strip = True
                continue
            if re.match( self.comment_begin_mark, line ) or self.__in_comment:
                # skipping all the commented lines "{#"{line}["#}"]
                self.__in_comment = True
                if re.match( self.comment_end_mark, line ):
                    self.__in_comment = False
                template_code.append(self.__indentation + '## %s' % (line))
                continue
            if( re.match( self.indent_regex, line ) ):
                mark, out_var = re.match(self.indent_regex, line).groups()
                self.__indentation = " " * len(
                    re.match(r'\s*', mark ).group())
                if re.match(self.in_code_mark, mark):
                    self.__in_code = True
                elif re.match(self.out_code_mark, mark):
                    self.__in_code = False
                    if out_var:
                        template_code.append(
                            self.__indentation + '{} = "".join({})'.format(
                                self.out_var, self.out_var))
                        try:
                            assert out_var == self.out_var
                        except Exception:
                            sys.stderr.write(
                                "ERROR\n"
                                "Output var mismatch\nfile: %s\nline:%s\n"
                                "%s != %s\n" % (
                                    template_src_file_name, idx_line,
                                    out_var, self.__out_var))
                            sys.exit(1)
                        self.__out_var.pop()
                elif re.match(self.new_var_mark, mark):
                    self.__in_code = False
                    assert out_var
                    self.__out_var.append(out_var)
                    template_code.append(
                        self.__indentation + '{} = []'.format(self.out_var))
                template_code.append( line )
                continue
            if not self.__in_code:
                template_code.append(
                    self.__indentation + self.__pythonized_code_line(line))
                continue
            template_code.append(line)
        return template_code

    def dans_template(self, template_src_file_name = None):
        template_code = self.__gen_code()
        result = []
        result.append("#-*- coding: utf-8 -*-")
        result.append(do_not_edit_msg % ( template_src_file_name or "?" ))
        result.append("from collorg.templates.template import _format")
        result.append("from collorg.templates.document_type.html import Html")
        result.append("from collorg.controller.controller import _template")
        if self.__pragma:
            result.append(
                'PRAGMA = {{\n {pragma} }}\n'.format(
                    pragma=",\n ".join( self.__pragma)))
        else:
            result.append('PRAGMA = {}')
        result.append("@_template")
        result.append("def {}( self, cog_charset, cog_user, cog_environment, **kwargs):".format(
            self.__template_name))
        result.append('    _ = self.db._cog_controller.i18n.gettext')
#        result.append('    if "cog_pre" in self.__class__.__dict__:')
#        result.append('         return')
#        result.append('        ok = self.cog_pre(cog_charset, cog_user, cog_environment, **kwargs)')
#        result.append('        if not ok: return')
        result.append('    html = Html( self )')
        result.append(
            "    self._cog_html_id = html.set_html_id(self, '{}')".format(
            self.__template_name))
        result.append('    {} = []'.format(self.out_var))
        for line in template_code:
            result.append("    {}".format(line))
        assert self.__out_var == [self.default_out_var]
        result.append("    if 'format' in PRAGMA.keys():")
        result.append(
            "        {} = _format(PRAGMA['format'], {}, cog_charset)".format(
            self.default_out_var, self.default_out_var))
        result.append('    return "".join({})'.format(self.default_out_var))
        result = "\n".join([elt.decode(self.__charset) for elt in result])
        try:
            return str(result)
        except:
            return result.encode(self.__charset)

    def parse( self,
               template_name, template_src, template_src_file_name = None ):
        self.__template_name = template_name
        self.__template_lines = [
            line.rstrip() for line in template_src.split( "\n" ) ]
        return self.dans_template( template_src_file_name )
