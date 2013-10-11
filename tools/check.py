#!/usr/bin/env python
#-*- coding: utf-8 -*-

import getpass
import sys
import os
import socket

if sys.version_info.major < 3:
    input = raw_input

ok = True
mod_dep = [
    'setuptools','psycopg2','creole','networkx',
    'matplotlib','webob','configparser']

def check_dep():
    global ok
    for module in mod_dep:
        try:
            __import__(module)
        except:
            ok = False
            print("Missing {}".format(module))

def check_http_server():
    global ok
    s = socket.socket()
    http_serv = input('http server [localhost]: ').strip() or 'localhost'
    http_port = input('http port [80]: ').strip() or 80
    try:
        s.connect((http_serv, http_port))
    except:
        print("Can't connect to {}:{}".format(http_serv, http_port))
        ok = False

def psql_req(psql_cmd, req):
    global ok
    try:
        os.popen('{} template1 -c "{}"'.format(psql_cmd, req))
    except:
        ok = False

def check_db_access():
    def create_db():
        create_req = 'create database collorg_db_check template template1'
        psql_req(psql_cmd, create_req)
    def chk_extension():
        create_req = 'create extension intarray;drop extension intarray'
        psql_req(psql_cmd, create_req)
    def drop_db():
        drop_req = 'drop database collorg_db_check'
        psql_req(psql_cmd, drop_req)

    user = input('postgres user [{}]: '.format(pg_user)) or pg_user
    password = getpass.getpass()
    host = input('host [{}]: '.format(pg_host)).strip() or pg_host
    port = input('port [{}]: '.format(pg_port)).strip() or pg_port
    psql_cmd = 'export PGPASSWORD="{}";psql -U {} -h {} -p {}'.format(
        password, user, host, port)
    ok and create_db()
    ok and chk_extension()
    ok and drop_db()

def check_collorg_db_config():
    global ok
    try:
        open('/etc/collorg/collorg_db')
    except:
        print('Missing /etc/collorg/collorg_db config file')
        ok = False

if __name__ == '__main__':
    pg_user = 'collorg'
    pg_password = None
    pg_host = 'localhost'
    pg_port = 5432
    http_server = 'localhost'
    http_port = 80
    if not((sys.version_info.major == 2 and sys.version_info.minor >= 7) or
           sys.version_info.major >= 3):
        print("collorg need python 2.7 or greater")
        sys.exit(1)
    check_dep()
    ok and check_collorg_db_config()
    ok and check_db_access()
#    ok and check_http_server()
