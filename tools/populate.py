#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
from collorg.controller.controller import Controller
import ConfigParser

field_separator = '||'
fk_separator = '::'

def set_fk_val(field, val):
    f_field_name, val = val.strip().split(fk_separator)
    if f_field_name.find(".") == -1:
        f_table = field.f_table.db.table(field.f_table.fqtn)
    else:
        f_fqtn, f_field_name = f_field_name.rsplit('.', 1)
        f_table = field.f_table.db.table(f_fqtn)
#    print("1 XXXXX FK %s %s %s"%(f_table.fqtn, f_field_name, val))
    #print(list(f_table.__dict__))
    comp = 'ilike'
#    print("xxx %s" % f_table.__dict__[f_field_name].sql_type)
    if f_table.__dict__[f_field_name].sql_type.find('int') != -1:
        comp = '='
    f_table.__dict__[f_field_name].set_intention(val, comp)
#    print("2 XXXXX")
    return f_table.__dict__[f_field_name]

def set_val(obj, fields, line):
    vals = line.strip().split(field_separator)
    assert len(vals) == len(fields)
    idx = 0
    for val in vals:
#        print("0 XXXXX",fields[idx], obj.id, fields[idx]._cog_table.id)
        if(fk_separator in val):
            fk_field = set_fk_val(fields[idx],val)
            comp = 'ilike'
#            print("yyy %s" % fk_field.sql_type)
            if fk_field.sql_type.find('int') != -1:
                comp = '='
            fields[idx].set_intention(fk_field, comp)
        else:
            fields[idx].set_intention(val)
        for field in obj._cog_fields:
            if field.is_constrained:
                pass
#                print("1 XXXXX %s is set" % (field.name))
        idx += 1
    #print(obj.get_extent(just_return_sql = True))
    obj.insert()

def read_fields(obj, line):
    return [
        obj.__dict__[field_name]
        for field_name in line.strip().split(field_separator) ]

def insert_data(obj, lines):
    print(obj.fqtn)
    fields = read_fields(obj, lines.pop(0))
    for line in lines:
        if line[0] == '#':
            continue
        print(line.strip())
        set_val(obj, fields, line)

def add_data(schema,table):
    file_ = "./data/%s/%s" % ( schema, table )
    obj = database.table('%s.%s'%(schema, table))
    lines = open(file_).readlines()
    if len(lines):
        insert_data(obj,lines)

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read( 'init.cfg' )
    if len(sys.argv) == 1:
        db_name = config.sections()[0]
        items = config.items(db_name)
    else:
        items = [tuple(sys.argv[1].rsplit("."))]
    database = Controller().db
    db_name = database.name
    for item in items:
        schemaname = item[0]
        tablenames = item[1]
        print( "schema: %s" % ( schemaname ) )
        for tablename in tablenames.split( '\n' ):
            if tablename:
                fqtn = "%s.%s" % ( schemaname, tablename )
                print( " + %s" % ( fqtn ) )
                type_ = database.table(
                    'collorg.core.data_type', fqtn_ = fqtn )
                if type_.count() == 0:
                    print( "   NEW" )
                    output = os.popen( "psql %s -f ./sql/%s/%s.sql 2>& 1" % (
                            db_name, schemaname, tablename ) ).readlines()
                    for line in output:
                        if line.find('ERROR') != -1:
                            print(line)
                    os.system("ocog make")
                    os.system('sudo python setup.py -q install')
                database = Controller(db_name).db
                try:
                    add_data(schemaname, tablename)
                except IOError:
                    print("no data")
