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
génère les schemas/modules d'une application à partir d'une base de
donnée. La base de donnée doit contenir la vue "collorg.core".db_struct
"""

import argparse
import os
import sys
from collorg.controller.controller import Controller
import collorg.utils.globvars as glob

if sys.version < '3':
    input = raw_input

def _input(question, default_val):
    question = "%s [%s]: " % (question, default_val)
    answer = input(question).strip()
    return answer or default_val



sql_version = "psql -qtc 'SELECT version()' %s | awk '{print $2}'"

sql_create_greater_9 = """
CREATE EXTENSION intarray;
CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION "unaccent";
CREATE OR REPLACE LANGUAGE plpgsql;
"""

class Init():
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--db_name", help = "database name")
        # [...] d'autres arguments
        # accessible via options.code_argument
        options = parser.parse_args(args)
        self.db_name = options.db_name
        self.pkg_path_1 = glob.cog_pkg_path(self.db_name)
        self.mod_path = self.pkg_path_1.replace("/", ".")
        in_cog_repo_db_name = glob._config('db', 'name')
        if in_cog_repo_db_name:
            sys.stderr.write(
                """you are in the '%s' collorg repository\n"""
                """you can't create a new repository in it\n"""
                """aborting\n""" % (
                    in_cog_repo_db_name))
            sys.exit(1)
        if os.path.exists("%s" % (self.db_name)):
            sys.stderr.write(
                "directory or file %s already in the way\n"
                "try cog make in that directory instead\n"
                "aborting\n" % (self.db_name))
            sys.exit(1)
        db_exists = os.popen(
            """psql --list | egrep '^ %s '""" % (
                self.db_name)).read().strip()
        if not db_exists:
            self.__create_db()
        self.__initdb()
        self.db = Controller(self.db_name).db
        self.charset = self.db._cog_controller._charset
        self.__make_cog_tree()
        self.db.table('collorg.core.data_type')._populate()

    def __get_db_connection_params(self):
        self.host = _input('host', 'localhost')
        self.port = _input('port', '5432')
        self.user = _input('user', 'collorg')
        self.password = input('password: ')
        self.__psql_cmd = "psql -h {host} -U {user} -p {port} -w".format(
            host = self.host, user = self.user, port = self.port)
        self.__db_psql_cmd = "psql -h {host} -U {user} -p {port} {name} -w"\
            .format(
                host = self.host, user = self.user, port = self.port,
                name = self.db_name)

    def __create_cog_ini_file(self):
        raise NotImplementedError
        try:
            open("/etc/collorg/%s" % (self.db_name))
            return
        except:
            pass
        charset = _input('charset', 'utf-8')
        file_ = app_ini_file.format(
            name = self.db_name,
            user = user, password = password, host = host, port = port,
            charset = charset)
        open("/etc/collorg/%s" % (self.db_name), "w").write(file_)



    def __check_pg_extensions(self):
        pg_config_present = os.popen('which pg_config').read().strip()
        try:
            assert pg_config_present
        except:
            sys.stderr.write("can't find pg_config!\naborting\n")
            sys.exit(1)
        pg_version = os.popen(sql_version % self.db_name).read()
        pg_release, pg_sub_release = pg_version.strip().split(".")[:2]
        self.pg_release = int(pg_release)
        self.pg_sub_release = int(pg_sub_release)
        self.pg_sharedir = os.popen("pg_config --sharedir").read().strip()

    def __create_db(self):
        self.__check_pg_extensions()
        if sys.version < '3':
            create = raw_input("will try to create %s database [y/N]? " % (
                self.db_name))
        else:
            create = input("will try to create %s database [y/N]? " % (
                self.db_name))
        if create.upper() != 'Y':
            print("aborting")
            sys.exit()
        exit_status = os.system(
            "createdb %s --owner collorg" % (self.db_name))
        if exit_status != 0:
            sys.stderr.write("unable to create database %s\n%s\n" % (
                    self.db_name, exit_status))
            sys.exit(exit_status)

    def __check_uuid(self):
        import uuid
        try:
            uuid_val = os.popen(
                """psql %s -qtc "SELECT uuid_generate_v1()" """
                """2> /dev/null """ % (
                    self.db_name)).read().strip()
            uuid.UUID(uuid_val)
            return True
        except:
            return False

    def __check_intarray(self):
        try:
            os.popen("""psql %s -qtc "SELECT icount('{1,2,3}'::int[])" """ % (
                self.db_name))
            return True
        except:
            return False

    def __initdb(self):
        """
        ajoute à la base les infos nécessaires pour un usage collorg
        * extension intarray
        * extension uuid-ossp
        * plpgsql
        """
        if self.__check_uuid() and self.__check_intarray():
            return
        self.__check_pg_extensions()
        print("adding the necessary extensions to the database")
        try:
            assert self.pg_release >= 9 or (
                self.pg_release >= 8 and self.pg_sub_release >= 4)
        except:
            sys.stderr.write("need postgresql 8.4 or greater\n"
                              "got %s.%s instead. aborting\n" % (
                    self.pg_release, self.pg_sub_release))
            sys.exit(1)
        if self.pg_release < 9 or self.pg_sub_release == 0:
            # intarray et uuid-ossp sont-il installés
            intarray = "%s/contrib/_int.sql" % (self.pg_sharedir)
            uuid_ossp = "%s/contrib/uuid-ossp.sql" % (self.pg_sharedir)
            if not os.path.exists(intarray):
                sys.stderr.write(
                    "can't find intarray extension\n"
                    "unable to read %s" % (intarray))
                sys.exit()
            if not os.path.exists(uuid_ossp):
                sys.stderr.write(
                    "can't find uuid-ossp extension\n"
                    "unable to read %s" % (uuid_ossp))
                sys.exit()
            cmd = sql_create_less_9_1 % (
                    self.db_name, intarray,
                    self.db_name, uuid_ossp,
                    self.db_name)
            os.system(cmd)
        else:
            os.popen("psql %s -qtc '%s'" % (
                    self.db_name, sql_create_greater_9))
        print("please, re-run 'cog init -d %s' to finish the installation" % (
                self.db_name))
        sys.exit()

    def __make_cog_tree(self):
        db_name = self.db_name
        base_dir = "%s" % (db_name)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
            open("%s/__init__.py" % (base_dir), "w")
            if not os.path.exists("%s/.cog" % (base_dir)):
                os.mkdir("%s/.cog" % (base_dir))
                open("%s/.cog/config" % (base_dir), "w").write(
                    glob.cog_config % (db_name))
        os.chdir(base_dir)
        abs_base_dir = os.path.abspath(os.path.curdir)
        sys.path.insert(0, abs_base_dir)
        cog_app_pkg_dir = self.pkg_path_1
        if not os.path.exists(cog_app_pkg_dir):
            os.makedirs(cog_app_pkg_dir)
            os.makedirs("%s/_cog_web_site/__src" % cog_app_pkg_dir)
            open("%s/__init__.py" % (self.pkg_path_1), "w")
            open("%s/_cog_web_site/__init__.py" % (
                cog_app_pkg_dir), "w")
        open("%s/__init__.py" % (cog_app_pkg_dir), "w")
        os.chdir(cog_app_pkg_dir)
        for schema in self.db.schemas:
            if schema.name.find("collorg.") == 0:
                continue
            if not os.path.exists(schema.name):
                os.mkdir(schema.name)
                open("%s/__init__.py" % (schema.name), "w")
                os.makedirs("%s/%s" % (schema.name, glob.templates_dir))
                open("%s/%s/__init__.py" % (
                        schema.name, glob.templates_dir), "w")
            os.chdir(schema.name)
            for tablename in schema.tables:
                fqtn = "%s.%s" % (schema.name, tablename)
                module = self.db.table(
                    'collorg.core.data_type',
                    fqtn_ = fqtn,
                    name_ = tablename)
                if not module.exists():
                    module.insert()
                if not os.path.exists("%s.py" % (tablename)):
                    print("+ %s.%s" % (schema.name, tablename))
                    fd = open("__init__.py", "w")
                    fd.write(glob.module_template % (
                            self.charset,
                            tablename.capitalize(),
                            schema.name, tablename,
                            tablename.capitalize()))
                    fd.close()
                if not os.path.exists("%s/%s" % (
                        glob.templates_dir, tablename)):
                    os.makedirs("%s/%s" % (
                            glob.templates_dir, tablename))
                    open("%s/%s/__init__.py" % (
                            glob.templates_dir, tablename), "w")
                    open("%s/cog/__init__.py" % (tablename), "w")
                    os.makedirs("%s/__src/%s" % (
                            glob.templates_dir, tablename))
            os.chdir('..')
        os.chdir(abs_base_dir)
        if False:#not os.path.exists("setup.py"):
            #FIXME this is not working
            if not os.path.exists(".cog"):
                os.mkdir('.cog')
                open('.cog/config', "w").write(
                    glob.cog_config_template % (self.db_name))
            fd = open("setup.py", "w")
            fd.write(glob.setup_template % (self.pkg_path_1, self.db_name))
            fd.close()
        print("%s library generated.\n"
               "you can now go to the %s directory and\n"
               "'python setup.py -q install' to install it" % (
                self.db_name, self.db_name))
