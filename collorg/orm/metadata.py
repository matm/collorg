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
from collections import OrderedDict

sql_db_struct = """
SELECT
    a.attrelid AS tableid,
    array_agg( i.inhseqno::TEXT || ':' || i.inhparent::TEXT ) AS inherits,
--    db.datname AS database_name,
--    db.encoding AS database_encoding,
    c.relkind AS tablekind,
    n.nspname AS schemaname,
    c.relname AS tablename,
    tdesc.description AS tabledescription,
    a.attname AS fieldname,
    adesc.description AS fielddescription,
    a.attndims AS fielddim,
    pt.typname AS fieldtype,
    a.attnum AS fieldnum,
    NOT( a.attislocal ) AS inherited,
    cn_uniq.contype AS uniq,
    a.attnotnull OR NULL AS notnull,
    cn_pk.contype AS pkey,
    cn_fk.contype AS fkey,
    cn_fk.conname AS fkeyname,
    cn_fk.conkey AS keynum,
    cn_fk.confrelid AS fkeytableid,
    cn_fk.confkey AS fkeynum,
    -- mettre le nom de la clef référencée en clair
    n_fk.nspname AS fk_schemaname,
    c_fk.relname AS fk_tablename,
    a_fk.attname AS fk_fieldname
FROM
    pg_class c -- table
    LEFT JOIN pg_description tdesc ON
    tdesc.objoid = c.oid AND
    tdesc.objsubid = 0
    LEFT JOIN pg_namespace n ON
    n.oid = c.relnamespace
--    LEFT JOIN pg_tablespace t ON
--    t.oid = c.reltablespace
--    JOIN pg_database db ON
--    db.dattablespace = t.oid
    LEFT JOIN pg_inherits i ON
    i.inhrelid = c.oid
    LEFT JOIN pg_attribute a ON
    a.attrelid = c.oid
    LEFT JOIN pg_description adesc ON
    adesc.objoid = c.oid AND
    adesc.objsubid = a.attnum
    JOIN pg_type pt ON
    a.atttypid = pt.oid
    LEFT JOIN pg_constraint cn_uniq ON
    cn_uniq.contype = 'u' AND
    cn_uniq.conrelid = a.attrelid AND
    a.attnum = ANY( cn_uniq.conkey )
    LEFT JOIN pg_constraint cn_pk ON
    cn_pk.contype = 'p' AND
    cn_pk.conrelid = a.attrelid AND
    a.attnum = ANY( cn_pk.conkey )
    LEFT JOIN pg_constraint cn_fk ON
    cn_fk.contype = 'f' AND
    cn_fk.conrelid = a.attrelid AND
    a.attnum = ANY( cn_fk.conkey )
    -- les réf. clef étrangères en clair
    LEFT JOIN pg_class c_fk ON
    c_fk.oid = cn_fk.confrelid
    LEFT JOIN pg_namespace n_fk ON
    n_fk.oid = c_fk.relnamespace
    LEFT JOIN pg_attribute a_fk ON
    a_fk.attrelid = c_fk.oid AND
    a_fk.attnum = cn_fk.confkey[idx( cn_fk.conkey, a.attnum )]
WHERE
    n.nspname <> 'pg_catalog'::name AND
    n.nspname <> 'information_schema'::name AND
    ( c.relkind = 'r'::"char" OR c.relkind = 'v'::"char" ) AND
    a.attnum > 0 -- AND
    -- c.relkind = 'r' -- A SUPPRIMER POUR INTEGER LES VUES
GROUP BY
    a.attrelid,
--    db.datname,
--    db.encoding,
    n.nspname,
    c.relname,
    tdesc.description,
    c.relkind,
    a.attnum,
    a.attname,
    adesc.description,
    a.attndims,
    a.attislocal,
    pt.typname,
    cn_uniq.contype,
    a.attnotnull,
    cn_pk.contype,
    cn_fk.contype,
    cn_fk.conname,
    cn_fk.conkey,
    cn_fk.confrelid,
    cn_fk.confkey,
    n_fk.nspname,
    c_fk.relname,
    a_fk.attname
ORDER BY
    a.attrelid,
    c.relkind,
    a.attnum, n.nspname, c.relname ;
"""

class TableMetadata:
    pass

class SchemaMetadata:
    pass

class DbMetadata:
    pass

class Metadata:
    """
    db_struct fait référence à la vue collorg.db_struct contentant la desciption
    des schemas, tables, champs de la base.
    cette vue est interrogée une fois à la connexion à la base de données
    self.__metadata est un dictionnaire organisé comme suit :
    * self.__metadata[schema]
    """
    def __init__( self, db ):
        self.__db_struct = db.get_query_res( sql_db_struct )
        d_schemas = OrderedDict()
        l_schemas = []
        #d_fkeys = OrderedDict()
        d_oid_table = OrderedDict() # dict sur [tableid]
        d_fqtn_table = OrderedDict() # dict sur [fqtn]
        d_oid_field = OrderedDict() # dict sur [tableid][fieldnum]
        for tpl in self.__db_struct:
            tableid = tpl['tableid']
            inherits = []
            if not None in tpl['inherits']:
                for elt in tpl['inherits']:
                    elt_id = elt.split( ':' )[1]
                    inherits.append( int( elt_id ) )
            #tablekind = tpl['tablekind']
            schemaname = tpl['schemaname']
            tablename = tpl['tablename']
            fieldname = tpl['fieldname']
            fqtn = ( '%s.%s' % ( schemaname, tablename ) )
            sql_fqtn = ( '"%s"."%s"' % ( schemaname, tablename ) )
            sql_fqfn = ( '%s."%s"' % ( sql_fqtn, fieldname ) )
            if not tableid in d_oid_table:
                d_fqtn_table[fqtn] = tableid
                d_oid_table[tableid] = {
                    'inherits':inherits,
                    'tablekind':tpl['tablekind'],
                    'schemaname':tpl['schemaname'],
                    'tablename':tpl['tablename'],
                    'description':tpl['tabledescription'],
                    'sql_fqtn':sql_fqtn,
                    'fqtn':fqtn }
            if not None in tpl['inherits']:
                for elt in tpl['inherits']:
                    elt_id = int(elt.split( ':' )[1])
                    if not 'children_fqtns' in d_oid_table[elt_id]:
                        d_oid_table[elt_id]['children_fqtns'] = []
                    if not d_oid_table[tableid]['fqtn'] in \
                        d_oid_table[elt_id]['children_fqtns']:
                            d_oid_table[elt_id]['children_fqtns'].append(
                                d_oid_table[tableid]['fqtn'])
            if not schemaname in d_schemas:
                d_schemas[schemaname] = OrderedDict()
                d_schemas[schemaname]['d_tbl'] = OrderedDict()
                d_schemas[schemaname]['l_tbl'] = []
                l_schemas.append( schemaname )
            if not tablename in d_schemas[schemaname]['d_tbl']:
                d_schemas[schemaname]['l_tbl'].append( tablename )
                d_schemas[schemaname]['d_tbl'][tablename] = {
                    'schemaname': schemaname,
                    'tablename': tablename,
                    'tableid': tableid,
                    'l_fld': [],
                    'd_fld': OrderedDict(),
                    }
                d_oid_field[tableid] = OrderedDict()
            d_field = OrderedDict()
            for metadata_fieldname in [
                'fieldname',
                'fielddescription',
                'fieldtype',
                'fielddim',
                'fieldnum',
                'inherited',
                'uniq',
                'notnull',
                'pkey',
                'fkey',
                'keynum',
                'fkeyname',
                'fkeytableid',
                'fkeynum' ]:
                d_field[metadata_fieldname] = tpl[metadata_fieldname]
            if d_field['fieldname'] == 'cog_oid':
                d_field['fkey'] = ''
                d_field['fkeyname'] = ''
                d_field['fkeytableid'] = ''
                d_field['fkeynum'] = ''
            d_field['fqtn'] = fqtn
            d_field['fqfn'] = sql_fqfn
            d_oid_field[tableid][tpl['fieldnum']] = d_field
            d_schemas[schemaname]['d_tbl'][tablename]['l_fld'].append(
                fieldname )
            d_schemas[schemaname]['d_tbl']\
                [tablename]['d_fld'][fieldname] = d_field
        self.__metadata = d_schemas
        self.__l_schemas = l_schemas
        self.__d_fkeys = self.__set_d_fkeys( d_oid_field )
        self.d_oid_table = d_oid_table
        self.d_fqtn_table = d_fqtn_table
        for sch in d_schemas:
            for tbl in d_schemas[sch]['d_tbl']:
                dtbl = d_schemas[sch]['d_tbl'][tbl]
                dtbl['children_fqtns'] = []
                if 'children_fqtns' in d_oid_table[dtbl['tableid']]:
                    dtbl['children_fqtns'] = \
                        d_oid_table[dtbl['tableid']]['children_fqtns']

    def __set_d_fkeys( self, doid ):
        d_fkey = OrderedDict()
        for key in doid:
            for key2 in doid[key]:
                doid2 = doid[key][key2]
                if doid2['fkey'] != 'f':
                    continue
                fqtn = doid2['fqtn']
                fieldname = doid2['fieldname']
                idx_field = doid2['keynum'].index(doid2['fieldnum'])
                fkeynum = doid2['fkeynum'][idx_field]
                fkeytableid = doid2['fkeytableid']
                fk_fqtn = doid[fkeytableid][fkeynum]['fqtn']
                if fk_fqtn == 'collorg.core.oid_table' and fieldname == 'cog_oid':
                    continue
                fk_fieldname = doid[fkeytableid][fkeynum]['fieldname']
                if not fqtn in d_fkey:
                    d_fkey[fqtn] = OrderedDict()
                if not fk_fqtn in d_fkey[fqtn]:
                    d_fkey[fqtn][fk_fqtn] = OrderedDict()
                d_fkey[fqtn][fk_fqtn][fieldname] = fk_fieldname
        return d_fkey

    def schemas_names( self ):
        return self.__l_schemas

    def tables_names( self, schemaname ):
        return self.__metadata[schemaname]['l_tbl']

    def fields_names( self, schemaname, tablename ):
        try:
            return self.__metadata[schemaname]['d_tbl'][tablename]['l_fld']
        except:
            raise RuntimeError("ERROR metadata.fields_names! %s.%s" % (
                schemaname, tablename))

    @property
    def metadata(self):
        return self.__metadata

    def d_field( self, schemaname, tablename, fieldname ):
        return self.__metadata[schemaname]['d_tbl']\
            [tablename]['d_fld'][fieldname]

    def d_schema( self, schemaname ):
        return self.__metadata[schemaname]

    def d_table( self, schemaname, tablename ):
        return self.__metadata[schemaname]['d_tbl'][tablename]

    @property
    def d_fkey( self ):
        return self.__d_fkeys

    @property
    def new_d_fkey( self ):
        return self.__new_d_fkeys

    def children_fqtns(self, schemaname, tablename):
        return self.__metadata[schemaname]['d_tbl'][tablename]['children_fqtns']

    def __iter__( self ):
        for key in self.__metadata:
            yield self.__metadata[key]

    def __str__( self ):
        return "%s" % ( self.__metadata )
