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
La connection se contente de charger le squelette de la base
db.schema.table sans instancier "complètement" les objets correspondants
aux tables. C'est au moment de l'instanciation que les champs seront
"accrochés". -> gain de temps.
Le graphe de la base est construit à la connexion.
"""

import sys
from datetime import datetime
import networkx as nx
import traceback
import os

#from collorg.utils.deco import benchmark, logging, counter, trace
from .metadata import Metadata
from .schema import Schema
import psycopg2.extras

class Db( object ):
    """
    blah
    """
    __d_tables = {}
    __debug = True
    def __init__( self, controller, db_name, _db, cursor, params ):
        """
        """
        self.__name = db_name
        self.db = _db
        self.__cursor = cursor
        self._cog_params = params
        if self._cog_params['debug']:
            self.__debug = True
        self.__test_mode = False
        self.__transaction = []
        self._d_r_neigh = {}
        self._cog_controller = controller
        sys.stderr.write( "[collorg][%s] %s\n" % (
            self.__name, datetime.now().isoformat() ) )
        self.__auto_commit = True
        self._metadata = Metadata( self )
        self._di_graph = self.__set_graph()
        self._graph = nx.Graph( self._di_graph )
        self.__l_schemas_names = []
        for schema in self._metadata.schemas_names():
            self.__l_schemas_names.append( schema )
            self.__add_schema( schema )

    def close(self):
        self.db.close()

    @property
    def cursor(self):
        return self.__cursor

    def new_cursor(self):
        self.__cursor = self.db.cursor(
            cursor_factory = psycopg2.extras.DictCursor)

    def close_cursor(self):
        self.__cursor.close()

    def __get_test_mode(self):
        return self.__test_mode

    def __set_test_mode(self, mode = True):
        assert mode in (True, False)
        if mode is True:
            print("Going into test mode.")
        if mode is False:
            bt = self.table('collorg.core.base_table')
            bt.cog_test_.set_intention(True)
            bt.cog_signature_.set_intention(id(self))
            print("Out of test mode. Removing %s test tuples." % bt.count())
            bt.delete()
        self.__test_mode = mode

    test_mode = property(__get_test_mode, __set_test_mode)

    def __del__( self ):
        self.__cursor.close()

    def __set_graph( self ):
        """
        constructs the directed graph representing the database
        """
        heavy_nodes = [ 'collorg.core.data_type' ]
        di_graph = nx.DiGraph()
        d_fkey = self._metadata.d_fkey
        for fqtn in d_fkey:
#            print("XXXXX", fqtn,d_fkey[fqtn])
            for fk_fqtn, l_fields in d_fkey[fqtn].items():
                src = fqtn
                dst = fk_fqtn
                weight = 1
                if src in heavy_nodes or dst in heavy_nodes:
                    weight = 100
                di_graph.add_edge( src, dst )
                di_graph[src][dst]['weight'] = weight
                di_graph[src][dst]['l_fields'] = l_fields
                if not dst in self._d_r_neigh:
                    self._d_r_neigh[dst] = {}
                if not src in self._d_r_neigh[dst]:
                    self._d_r_neigh[dst][src] = []
                self._d_r_neigh[dst][src] = l_fields
        return ( di_graph )

    def neighbors(self, fqtn):
        """returns only directs neighbors"""
        try:
            return self._di_graph[fqtn]
        except:
            return {}

    def rev_neighbors(self, fqtn):
        try:
            return self._d_r_neigh[fqtn]
        except:
            return {}

    def _neigh(self, fqtn):
        try:
            d_neigh = self.d_neigh[fqtn]
        except:
            d_neigh = {}
        try:
            d_r_neigh = self.d_r_neigh[fqtn]
        except:
            d_r_neigh = {}
        return d_neigh, d_r_neigh

    def _path(self, start_obj, end_obj):
        graph = self._graph
        di_graph = self._di_graph
        if( start_obj.fqtn == end_obj.fqtn and
            nx.has_path( di_graph, start_obj.fqtn, end_obj.fqtn ) ):
                path = [start_obj.fqtn]
        elif nx.has_path( di_graph, start_obj.fqtn, end_obj.fqtn ):
            path = nx.shortest_path(
                di_graph, start_obj.fqtn, end_obj.fqtn, 'weight' )
        else:
            path = nx.shortest_path(
                graph, start_obj.fqtn, end_obj.fqtn, 'weight' )
        return path

    def _get_path( self, start_obj, end_obj ):
        """
        @return: a list of dictionary giving a shortest path between
        start_obj and end_obj.
        les premiers seront les...
        """
#        print("0 XXXXX %s.join(%s)" % (end_obj, start_obj))
        from .field import Field
        graph = self._graph
        di_graph = self._di_graph
        if start_obj.__class__ is Field:
            start_obj = start_obj._cog_table
        path = self._path(start_obj, end_obj)
        ret_path = []
        idx = 0
        for elt in path:
            this_elt = elt
            if idx == 0:
                this_elt
            next_ = {}
            if idx < len(path)-1:
                next_elt = path[idx+1]
                l_fields = graph.edge[elt][next_elt]['l_fields']
                if len(l_fields) > 1:
                    # the error message could be indicative
                    # which edge, what fields
                    raise RuntimeError("Ambiguous path %s in\n%s" % (
                        str(l_fields), path))
#                print("XXXXXXX",next_)
#                print("->>> YYYYY %s->%s" %(elt, next_elt)),
                if di_graph.has_edge(elt, next_elt):
                    src_field, dst_field = l_fields.items()[0]
                    next_['reverse'] = False
                else:
                    dst_field, src_field = l_fields.items()[0]
                    next_['reverse'] = True
                next_['src'] = {'fqtn':elt, 'field':src_field}
                next_['dst'] = {'fqtn':next_elt, 'field':dst_field}
                ret_path.append(next_)
#                print("1 YYYYY", next_)
            idx += 1
#        print("2 YYYYY",ret_path)
        return ret_path

    def _print_path(self, start_obj, end_obj, path):
        print("Path from %s to %s:" % (start_obj.fqtn, end_obj.fqtn))
        for elt in path:
            print( " * %s.%s %s %s.%s" % (
                elt['src']['fqtn'], elt['src']['field'],
                elt['reverse'] and "<-" or "->",
                elt['dst']['fqtn'], elt['dst']['field']))
        print("\n")

    def __add_schema( self, schemaname ):
        attr_schema = "%s_" % ( schemaname )
        if not self.has_schema( attr_schema ):
            self.__setattr__( attr_schema, Schema( self, schemaname ) )

    def has_schema( self, attr_schema ):
        """
        retourne vrai si le schéma est déjà rattaché au self
        """
        return attr_schema in self.__dict__

    @property
    def metadata( self ):
        return self._metadata

    def reload( self ):
        raise NotImplementedError

    # SQL

    def set_auto_commit( self, new_val ):
        assert new_val in ( False, True )
        self.__in_transaction = new_val
        self.__auto_commit = new_val

    def get_auto_commit(self):
        return self.__auto_commit

    def __log_sql(self, sql, duration, err=""):
        if self._cog_controller._debug:
            trace = traceback.extract_stack()[:-3]
            f = open("/tmp/cog_sql", 'a+')
            try:
                os.chmod("/tmp/cog_sql", 0777)
            except:
                pass
            f.write("{}\n{}\n{}\n{}\n".format(
                "{}{} {}s".format(err, 60 * "=", duration.total_seconds()),
                "\n".join(["{} {} {} {}".format(*elt) for elt in trace]),
                70*"-", sql))
            f.close()

    def commit( self, sql = "", just_return_sql = False):
        if not self.__auto_commit and not sql:
            self.__transaction.append( 'END' )
            self.set_auto_commit( True )
        sql = sql or ";\n".join( self.__transaction )
        if just_return_sql:
            self.set_auto_commit( True )
            return sql
        if not sql:
            self.set_auto_commit( True )
            return
        begin = datetime.now()
        try:
            self.__cursor.execute( sql )
            duration = datetime.now() - begin
        except Exception as err:
            duration = datetime.now() - begin
            self.rollback()
            self.set_auto_commit(False)
            self.__log_sql(sql, duration, "ERROR")
            raise Exception("Commit error! Rolling back!\n{}".format(err))
        self.__log_sql(sql, duration)
        self.set_auto_commit( True )
        self.__transaction = []
        self.db.commit()

    def fetchone(self, sql):
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()

    def rollback( self ):
        self.set_auto_commit( True )
        self.__transaction = []
        self.db.rollback()

    def raw_sql( self, sql_req, nodelay = False ):
        if( self.__auto_commit == False and
            not self.__transaction and
            not nodelay and
            not self.__in_transaction):
            self.__transaction.append( 'BEGIN' )
            self.__in_transaction = True
        self.__transaction.append( sql_req )
        if self.__auto_commit or nodelay:
            self.commit( nodelay and sql_req or "" )

    def get_query_res( self, sql_req, nodelay = False ):
        self.raw_sql( sql_req, nodelay = nodelay )
        return self.__cursor.fetchall()

    @property
    def name( self ):
        return self.__name

    @property
    def schemas_names( self ):
        return self.__l_schemas_names

    def _fqtn_2_sql_fqtn( self, fqtn ):
        return '"%s"' % ( '"."'.join( fqtn.rsplit( '.', 1 ) ) )

#    @counter
#    @trace
    def table( self, cog_fqtn, load_fields = True, *args, **kwargs ):
        """
        le fqtn est une chaîne de la forme : {db:}<schema>.<table>
        si db est spécifié, il s'agit d'une base distante [NI]
        si le nom du schéma débute par collorg, il s'agit du schema collorg
        exemple : table( 'a.b' )
        l'objet sera référencé par self.a_.b_ (PEP 8)
        """
        # sys.stderr.write( "DEBUG db.table %s\n" % cog_fqtn )
        if not cog_fqtn in self.__d_tables:
            cog_fqtn = cog_fqtn.replace( '"', '' )
            ( schema_name, table_name ) = cog_fqtn.rsplit( ".", 1 )
            if schema_name.find('collorg') == 0:
                mod_path_1 = 'collorg.db'
                schema_name = ".".join( schema_name.split( '.' )[1:] )
            else:
                mod_path_1 = "collorg_app.%s.db" % (self.__name)
            class_name = "%s" % table_name.capitalize()
            module_name = ".".join([mod_path_1, schema_name, table_name])
            temp = __import__(module_name, globals(), locals(), [''], -1)
            self.__d_tables[cog_fqtn] = temp.__dict__[class_name]
        return self.__d_tables[cog_fqtn](
            self, load_fields = load_fields, *args, **kwargs )

    def _set_controller(self, controller):
        self._cog_controller = controller

    @property
    def schemas( self ):
        for elt in self.__dict__:
            if self.__dict__[elt].__class__ is Schema:
                yield self.__dict__[elt]

    @property
    def tables( self ):
        for sch in self.schemas:
            for table in sch.tables:
                yield table

    @property
    def fqtns( self ):
        for sch in self.schemas:
            for fqtn in sch.fqtns:
                yield fqtn

    def get_elt_by_oid(self, cog_oid):
        """
        """
        return self.table(
            'collorg.core.base_table', cog_oid_ = cog_oid).get()

    def _sql_inherits(self, fqtn):
        """returns the list of fqtn inherited by self in db metadata"""
        res = []
        oid = self.metadata.d_fqtn_table[fqtn]
        for elt in self.metadata.d_oid_table[oid]['inherits']:
            res.append(self.metadata.d_oid_table[elt]['fqtn'])
        return res

    def showstruct(self, schema_name = None):
        schemas = list(self.schemas)
        schemas.sort()
        for schema in schemas:
            if schema_name is not None and schema_name != schema.name:
                continue
            print("\nSchema: %s\n" % schema.name)
            tables = list(schema.tables)
            tables.sort()
            for table in tables:
                print(" - %s" % table)
