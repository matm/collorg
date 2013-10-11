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

from .customerror import CustomError
from copy import deepcopy

class FieldIntention(object):
    __l_comp = [
        '=', '!=',
        '>', '>=', '<', '<=',
        'is', 'is not',
        'like', 'not like',
        'ilike', 'not ilike',
        '~', '~*', '!~', '!~*',
        'in', 'not in' ]
    def __init__(self, field):
        self.__field = field
        self.__val = None
        self.__raw_value = None
        self.__null = False # True if set_null or set_not_null !!
        self.__neg = False
        self.__quoted_val = ''
        self.__comp = '='
        self.__is_constrained = False
        self.__list = []

    def set_(self, val, comp = '='):
        self.__raw_value = val
        checked = False
        if val.__class__ is self.__field.__class__:
#            if id(val.table) == id(self.__field.table):
#                self.__is_constrained = True
#                return
            comp = 'IN'
            if (self.__field.is_fkey and
                self.__field.f_table.fqtn == val._cog_table.fqtn):
                    checked = True
        try:
            assert comp.lower() in FieldIntention.__l_comp
        except:
            raise CustomError(
                "unknow comparator '%s'\n"
                "known comparators are: %s" % (
                    comp, FieldIntention.__l_comp))
        if val is None:
            self.__val = None
            self.__is_constrained = False
            return
        self.__null = False
        self.__is_constrained = True
        self.__comp = comp
        if not checked:
            val = self.__field._cog_ref_type.check(self.__field, val)
            if val is None:
                # wiered but we get here in case of rel.join(rel)
                self.__is_constrained = False
                return
        self.__val = val
        self.__quoted_val = self.quoted_val

    def set_null(self):
        self.__val = "NULL"
        self.__comp = "IS"
        self.__null = True
        self.__is_constrained = True

    def set_not_null(self):
        self.__val = "NULL"
        self.__comp = "IS NOT"
        self.__null = True
        self.__is_constrained = True

    @property
    def is_constrained(self):
        return self.__is_constrained

    @property
    def comp(self):
        return self.__comp

    @property
    def val(self):
        return self.__val

    @property
    def value(self):
        return self.__raw_value

    @property
    def quoted_val(self):
        """
        @return: the escaped SQL value.
        @raise exception: if the value can't be escaped.
        """
        if not self.__is_constrained:
            return None
        val = self.__val
        if not self.__null:
            if val.__class__ is self.__field.__class__:
                table = val.table
                ref_field = val
                if self.__field.is_fkey:
                    ref_field = table.__dict__[self.__field.f_fieldname]
                val = "\n(\n%s)" % (table._cog_new_select([ref_field]))
                return val
            elif type(self.__val) != bool and self.__val is not None:
                val = str(self.__val).replace("'", "''")#.replace("\\", "\\\\")
                return "'%s'" % (val)
            elif type(val) is bool:
                if val:
                    return "'t'"
                return "'f'"
        else:
            return val
        raise RuntimeError("Not here! %s\n" % (val))

    def __single_sql_where_repr(self):
        val = self.quoted_val
        if val is None:
            return None
        field_name = self.__field.id_name
        comp = self.comp
        if self.__field.unaccent:
            field_name = "unaccent(%s)" % field_name
            val = "unaccent(%s::text)" % val
        res = " ".join([field_name, comp, val])
        return res

    def _sql_where_repr(self, res = ""):
        res = self.__single_sql_where_repr()
        for intention, op_ in self.__list:
            res = "(%s %s %s)" % (res, op_, intention._sql_where_repr(res))
        if self.__neg:
            res = "not(%s)" % (res)
        return res

    def __call__(self):
        return deepcopy(self)

    def __repr__(self):
        #!! conversion systématique en str ?
        return str(self.__val)

    def __op(self, other, _op_):
        self.__list.append((other, _op_))
        return self

    def __iop(self, _op_, val, comp):
        if not self.is_constrained:
            self.set_(val, comp)
        else:
            other = self.__class__(self.__field)
            other.set_(val, comp)
            self.__op(other, _op_)
        return self

    def __add__(self, other):
        self.__op(other, "or")
        return self

    def __iadd__(self, val, comp = 'IN'):
        if type(val) is tuple:
            val, comp = val
        self.__iop("or", val, comp)
        return self

    def __mul__(self, other):
        self.__op(other, "and")
        return self

    def __imul__(self, val, comp = 'IN'):
        if type(val) is tuple:
            val, comp = val
        self.__iop("and", val, comp)
        return self

    def __sub__(self, other):
        print("SUB")
        self.__op(other, "and not")
        return self

    def __isub__(self, val, comp = 'IN'):
        if type(val) is tuple:
            val, comp = val
        self.__iop("and not", val, comp)
        return self

    def __neg__(self):
        self.__neg = not self.__neg
