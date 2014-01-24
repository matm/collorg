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

import sys
import uuid
import datetime
from .customerror import CustomError

if sys.version >= "3":
    unicode = str

class PgType( object ):
    __d_pg_types = {
        # numeric types
        'smallint':int,
        'integer':int,
        'int2':int,
        'int4':int,
        'int8':int,
        'bigint':int,
        'decimal':int,
        'serial':int,
        'bigserial':int,
        'numeric':float,
        'real':float,
        'float8':float,
        'double precision':float,
        # character types
        'character varying':str,
        'varchar':str,
        'character':str,
        'char':str,
        'bpchar':str,
        'text':str,
        'password':str,
        'wiki':str,
        'string':str,
        'c_fqtn':str,
        'email':str,
        'url':str,
        # date/time types
        'timest':'iso_timestamp',
        'timestamp':'iso_timestamp',
        'date':'iso_date',
        'year':int,
        'month':int,
        'day':int,
        'hour':int,
        'minute':int,
        # boolean type
        'boolean':bool,
        'bool':bool,
        # enumerated type ?
        # network addr types ( http://www.python.org/dev/peps/pep-3144/ )
        'cidr':str,
        'inet':'notImplemented',
        'macaddr':'notImplemented',
        # uuid types
        'c_oid':'checkUUID',
        'uuid':'checkUUID',
        # binary
        'bytea':bytes,
        'notImplemented':'notImplemented' # pour les tests
        }

    def __init__( self, sql_type ):
        if sql_type[0] != '_':
            self.__type = PgType.__d_pg_types[sql_type]
        else:
            self.__type = list

    def __repr__( self ):
        return "%s" % ( self.__type )

    def __check_array(self, field, val):
        #XXX BUGGY: use with extra caution!
        # strings containing any of "{}[]" characters will make this fail...
        # The solution lies in relation.py by refactoring the construction
        # of the queries. RTFM of psycopg2...
        # REMEMBER! This is a prototype in pre-alpha development stage.
        sql_type = field.get_sql_type()[1:]
        array_ = [self.__d_pg_types[sql_type](elt) for elt in val]
        return "{}".format(array_).replace(
            "[", "{").replace("]", "}")

    def check( self, field, val ):
        """
        valide la compatibilité du type de la donnée par rapport au champ
        lève une exception en cas d'absence du type ou de non conversion
        """
        if type(val) is type(field):
            return val
        if val == None:
            return None
        sql_type = field.get_sql_type()
        if sql_type[0] == '_': #W redondant avec Field.__dimension ?
#            raise NotImplementedError
            sql_type = sql_type[1:] # les types array
        if not sql_type in self.__d_pg_types:
            raise CustomError("type Postgresql '%s' inconnu" % sql_type)
        if type(val) is self.__d_pg_types[sql_type]:
            return val
        if type(val) is unicode:
            val = val.encode(field._cog_table._cog_controller._charset)
        if(type(self.__d_pg_types[sql_type]) is str):
            if type(val) is unicode:
                val = val.encode(field._cog_table._cog_controller._charset)
            return self.__class__.__dict__[self.__d_pg_types[sql_type]](
                self, field, val)
        try:
            if field.get_sql_type()[0] != '_':
                return self.__d_pg_types[sql_type](val)
            else:
                return self.__check_array(field, val)
        except:
            raise RuntimeError(
                "Error pg_type.check: %s->%s with %s of type %s" % ( 
                    sql_type, self.__d_pg_types[sql_type], val,
                    val.__class__.__name__))

    def checkUUID( self, field, val ):
#        try:
#            uuid.UUID( str( val ) )
#        except Exception as err:
#            raise ValueError("%s: %s"%(err, val))
        return val

    def iso_timestamp( self, field, val ):
        """
        Sliced to the second
        """
        if type(val) in [datetime.date, datetime.datetime]:
            return "%s-%02d-%02dT%02d:%02d:%02dZ" % (
                val.year, val.month, val.day, val.hour, val.minute, val.second)
        return datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
        
    def iso_date( self, field, val ):
        """
        val is 
        the format must be iso8601. the "T%H:%M:%SZ" part is ignored
        """
        if type(val) in [datetime.date, datetime.datetime]:
            return "%s-%s-%s" % (val.year, val.month, val.day)
        return datetime.datetime.strptime(val, '%Y-%m-%d')
        
    def notImplemented( self, field, val ):
        sql_type = field.get_sql_type()
        raise CustomError(
                "Postgresql type '%s' non handled" % sql_type )

    @property
    def _type( self ):
        return self.__type
