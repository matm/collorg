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

class Schema( object ):
    def __init__( self, db, schemaname ):
        self.__name = schemaname
        self._metadata = db._metadata
        self.__tablenames = []
        self.__fqtns = []
        for tablename in db._metadata.tables_names( schemaname ):
            self.__tablenames.append( tablename )
            self.__fqtns.append( "%s.%s" % ( schemaname, tablename ) )

    @property
    def name( self ):
        return self.__name

    def has_table( self, tablename ):
        return tablename in self.__tablenames

    @property
    def tables( self ):
        for elt in self.__tablenames:
            yield elt

    @property
    def fqtns( self ):
        for elt in self.__fqtns:
            yield elt
