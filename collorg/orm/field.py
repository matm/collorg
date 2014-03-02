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

from collections import OrderedDict
from .pgtype import PgType
from .fieldintention import FieldIntention

class Field(object):
    def __init__(self, table, name):
        """
        """
        self.__table = table
        self.__rel_id = None
        self.__name = name
        self.__descending_order = ''
        self.__unaccent = False
        self.pyname = "%s_" % (name)
        self.fqfn = "%s.%s" % (table.fqtn, name)
        self.__name_as = name
        self.__f_table = None
        self.__intention = FieldIntention(self)
        if self.__d_metadata['fkeyname']: #fkey
            # on est sur une FK
            #!! pb de dépendance croisée ...
            d_t_oid = table.db.metadata.d_oid_table
            f_fqtn = "%s.%s" % (
                d_t_oid[self.__d_metadata['fkeytableid']]['schemaname'],
                d_t_oid[self.__d_metadata['fkeytableid']]['tablename'])
            if not(self.__name == 'cog_oid' and
                f_fqtn == 'collorg.core.oid_table'):
                self.__f_table = table.db.table(f_fqtn, load_fields = False)

    @property
    def __d_metadata(self):
        return self.__table.db._metadata.\
            metadata[self.__table._cog_schemaname]['d_tbl']\
            [self.__table._cog_tablename]['d_fld'][self.__name]

    def name_as(self, alias):
        self.__name_as = alias
        return self

    @property
    def id_name(self):
        return '"%s"."%s"' % (self.__rel_id or self.__table.id,self.__name)

    def _sql_where_repr(self, rel_id=None):
        self.__rel_id = rel_id
        return self.__intention._sql_where_repr()

    def set_descending_order(self):
        self.__descending_order = "DESC"

    @property
    def descending_order(self):
        return self.__descending_order

    def set_field_intention(self, field_intention, comp = 'IN'):
        """
        @field_intention: the field intention that will constrain this Field
        @comp: the comparator used (defaults to 'IN')
        """
        pass

    @property
    def _cog_table(self):
        return self.__table

    @property
    def _cog_dimension(self):
        return self.__d_metadata['fielddim']

    @property
    def sql_type(self):
        return self.__d_metadata['fieldtype']

    def get_sql_type(self): #XXX remove!
        return self.sql_type

    @property
    def _cog_ref_type(self):
        return PgType(self.sql_type)

    @property
    def ref_type(self):
        return PgType(self.sql_type)

    def matches(self, other):
        #W doit aussi comparer la compatibilité des types SQL ?
        return self.sql_type == other.sql_type

    @property
    def pkey(self):
        return self.__d_metadata['pkey']

    @property
    def sql_fqfn(self):
        """
        returns the Fully qualified field name :
        "<schemaname>"."<tablename>"."<fieldname>"
        """
        return '%s."%s"' % (self.__table.sql_fqtn, self.__name)

    @property
    def sql_name_as(self):
        """
        returns the Fully qualified field name :
        "<schemaname>"."<tablename>"."<fieldname>"
        """
        res = self.__name
        if self.__name != self.__name_as:
            res += " AS %s" % (self.__name_as)
        return res

    @property
    def orig_name(self):
        return self.__name

    @property
    def name(self):
        return self.__name_as

    @property
    def table(self):
        return self.__table

    @property
    def f_table(self):
        return self.__f_table

    @property
    def f_fieldname(self):
        if self.__f_table is None:
            return None
        return "%s_" % (
            self.__table.neighbors[self.__f_table.fqtn]['l_fields'][self.name])

    def __get_value(self):
        return self.__intention.value

    def __set_value(self, arg):
        """
        @val: a literal (compatible with the SQL type of self)
        @comp: the comparator used for this intention (defaults to '=')
        """
        val = arg
        comp = '='
        if type(arg) is tuple:
            val = arg[0]
            if len(arg) > 1:
                comp = arg[1]
        self.__intention.set_(val, comp)

    value = property(__get_value, __set_value)

    @property
    def comp(self):
        return self.__intention.comp

    @property
    def spec(self):
        res = OrderedDict()
        res['pkey'] = self.__d_metadata['pkey'] and "PK" or ""
        res['name'] = self.__name_as
        res['val'] = self.value or ""
        res['sql_type'] = self.sql_type
        res['inherited'] = self.__d_metadata['inherited'] and "inherited" or ""
        res['uniq'] = self.__d_metadata['uniq'] and "unique" or ""
        res['not_null'] = self.__d_metadata['notnull'] and "not null" or ""
        res['fkey'] = self.__d_metadata['fkeyname'] and "FK" or ""
        res['f_table'] = self.__f_table
        res['ftablelink'] = self.__d_metadata['fkeyname'] or ""
        res['fkeyname'] = self.__d_metadata['fkeyname'] or ""
        return res

    @property
    def is_fkey(self):
        return self.__f_table is not None

    @property
    def is_inherited(self):
        return self.__d_metadata['inherited']

    @property
    def is_required(self):
        return self.__d_metadata['notnull']

    def set_null(self):
        self.__intention.set_null()
        return self

    def set_not_null(self):
        self.__intention.set_not_null()
        return self

    def __call__(self):
        return Field(self.__table, self.__name)

    def copy(self):
        _cf = Field(self.__table, self.__name)
        _cf.__name_as = self.__name_as
        _cf.__d_metadata = self.__d_metadata
        _cf.__f_table = self.__f_table
        _cf.__intention = self.__intention()
        return _cf

    @property
    def is_constrained(self):
        return self.__intention.is_constrained

    def __get_unaccent(self):
        return self.__unaccent
    def __set_unaccent(self, boolean):
        pg_char_types = [
            'character varying','varchar','character','char',
            'bpchar','text','wiki','string','email']
        if self.sql_type in pg_char_types:
            self.__unaccent = boolean
        else:
            self.__unaccent = False

    unaccent = property(__get_unaccent, __set_unaccent)

    def __add__(self, other):
        self.__intention.__add__(other.__intention)
        return self

    def __iadd__(self, *args):
        self.__intention.__iadd__(*args)
        return self

    def __mul__(self, other):
        self.__intention.__mul__(other.__intention)
        return self

    def __imul__(self, *args):
        self.__intention.__imul__(*args)
        return self

    def __sub__(self, other):
        self.__intention.__sub__(other.__intention)
        return self

    def __isub__(self, *args):
        self.__intention.__isub__(*args)
        return self

    def __neg__(self):
        self.__intention.__neg__()
        return self

    def __eq__(self, arg):
        #!! à améliorer en utilisant la conversion selon de type du champ
        if arg is None:
            return self.value == None
        if arg.__class__ is Field:
            return self.value == arg.value
        else:
            return self._cog_ref_type._type(self.value) == \
                self._cog_ref_type._type(arg)

    def __ne__(self, arg):
        return not(self.__eq__(arg))

    def __gt__(self, arg):
        if arg.__class__ is Field:
            return self.value > arg.value
        else:
            return self._cog_ref_type._type(self.value) > \
                self._cog_ref_type._type(arg)

    def __lt__(self, arg):
        return not(self.__gt__(arg))

    def __ge__(self, arg):
        if arg.__class__ is Field:
            return self.value >= arg.value
        else:
            return self._cog_ref_type._type(self.value) >= \
                self._cog_ref_type._type(arg)

    def __le__(self, arg):
        return not(self.__ge__(arg))

    def quoted_val(self):
        return str(self.__intention.quoted_val())

    def __str__(self):
        return "{}".format(self.__intention.value).replace(
            '>', '&gt;').replace('<', '&lt;')
