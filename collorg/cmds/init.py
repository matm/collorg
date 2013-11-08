#!/usr/bin/env python
#-*- coding: utf-8 -*-

### Copyright © 2011-1012 Joël Maïzi <joel.maizi@lirmm.fr>
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

import argparse
import os
import sys
import psycopg2
import getpass
from collorg.controller.controller import Controller
import collorg.utils.globvars as glob

if sys.version < '3':
    input = raw_input

def _input(question, default_val):
    question = "%s [%s]: " % (question, default_val)
    answer = input(question).strip()
    return answer or default_val

sql_version = "SELECT version()"
sql_db_exists = "SELECT datname FROM pg_catalog.pg_database WHERE datname = %s"

app_ini_file = """[database]
user = {user}
password = {password}
host = {host}
port = {port}

[application]
charset = {charset}
#debug = True
templates_path = /usr/share/collorg/www/templates
url = collorg/{db_name}
url_scheme = http
production = True
upload_dir = /var/collorg/{db_name}
#user_photo_url =
session_cache_host = localhost
session_cache_port = 6543

[mail]
smtp_server = smtp.example.org
#smtp_port =
#smtp_user =
#smtp_password =
#default_user =
mail_prefix = [collorg]
error_report_to =
"""

cog_config_file = """[core]
database = %s
"""

create_db = """CREATE DATABASE %s OWNER %s"""
drop_db = """DROP DATABASE %s"""
create_user = """CREATE USER %s"""
drop_user = """DROP USER %s"""





class Cursor():
    def __init__(self, connexion):
        self.__connexion = connexion
        self.__cursor = self.__connexion.cursor()

    def __reset(self):
        self.__connexion.reset()
        self.__connexion.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def execute(self, sql, data = None):
        if data is None:
            return self.__cursor.execute(sql)
        return self.__cursor.execute(sql, data)

    def fetchall(self, sql, data = None):
        res = None
        try:
            self.execute(sql, data)
            res = self.__cursor.fetchall()
            self.__reset()
        except:
            self.__connexion.rollback()
        return res

    def fetchone(self, sql, data = None):
        res = None
        try:
            self.execute(sql, data)
            res = self.__cursor.fetchone()
            self.__reset()
        except Exception as err:
            print(err)
            self.__connexion.rollback()
        return res

    def fetchmany(self, sql, data = None, number = -1):
        res = None
        try:
            self.execute(sql, data)
            res = self.__cursor.fetchmany(number)
            self.__reset()
        except:
            self.__connexion.rollback()
        return res

class Cmd():
    def __init__(self, nop, *args):
        self.charset = 'utf-8'
        self.__curdir = os.path.abspath(os.path.curdir)
        parser = argparse.ArgumentParser(prog="cog init")
        parser.add_argument(
            "-d", "--db_name", required = True, help = "database name")
        options = parser.parse_args(*args)
        self.db_name = options.db_name
        self.__collorg_db = Controller('collorg_db').db
        self.__cursor = Cursor(self.__collorg_db.db)
        self.__check()
        self.__db_connection_params()
        db_exists = os.popen(
            """psql --list -U %s | egrep '^ %s '""" % (
            self.user, self.db_name)).read().strip()
        if not db_exists:
            self.__create_db()
        else:
            sys.stderr.write(
                "The database already exists\n"
                "Drop if you really want to proceed\n" )
            sys.exit(1)
        self.db = Controller(self.db_name).db
        self.charset = self.db._cog_controller._charset
        self.__make_cog_repos()

    def __check(self):
        try:
            collorg_repos = Controller()
        except RuntimeError:
            print("%s/%s" % (self.__curdir, self.db_name))
            if os.path.exists("%s/%s" % (self.__curdir, self.db_name)):
                sys.stderr.write(
                    "Directory or file %s already in the way.\n"
                    "Aborting!\n" % (self.db_name))
                sys.exit(1)
            self.__check_db_access()
            return
        sys.stderr.write(
            "Can't create a repos in a repos! "
            "You are currently in %s repos.\n" % collorg_repos.db.name)
        sys.exit()

    def __remove_check(self):
            try:
                self.__cursor.execute(drop_db % ('collorg_check'))
                self.__cursor.execute(drop_user % ('collorg_check'))
            except:
                pass

    def __check_db_access(self):
        try:
            # retreive postgresql version
            self.__pg_version = int(self.__cursor.fetchone(
                sql_version)[0].split()[1].split('.')[0])
            if self.__pg_version < 9:
                raise ValueError("Colorgs needs postgresql 9 or greater")
            # are we able to create a database
            self.__remove_check()
            self.__cursor.execute(create_user % ('collorg_check'))
            self.__cursor.execute(create_db % ('collorg_check','collorg_check'))
            assert(self.__cursor.fetchone(
                sql_db_exists, ('collorg_check',))[0] == 'collorg_check')
        except Exception as err:
            sys.stderr.write("%s\n" % err)
            # something went wrong. We stop here
            sys.exit()
        finally:
            self.__remove_check()

    def __db_connection_params(self):
        """
        sets the connection parameters to postgresql.
        the default paramaters come from self.__collorg_db.
        """
        self.user = _input('user', self.__collorg_db._cog_params['user'])
        self.host = _input('host', self.__collorg_db._cog_params['host'])
        self.port = _input('port', self.__collorg_db._cog_params['port'])
        if self.user != self.__collorg_db._cog_params['user']:
            while True:
                password1 = getpass.getpass('Enter password: ')
                password2 = getpass.getpass('Retype password: ')
                if password1 == password2:
                    self.password = password1
                    break
                print("Sorry, passwords do not match")
        else:
            self.password = self.__collorg_db._cog_params['password']
        self.cog_psql_cmd = "psql collorg_db -h {host} -U collorg -p {port} -w"\
            .format(
                host = self.host, user = self.user, port = self.port,
                name = self.db_name)
        self.__psql_cmd = "psql -h {host} -U {user} -p {port} -w".format(
            host = self.host, user = self.user, port = self.port,
            name = self.db_name)
        self.db_psql_cmd = "psql -h {host} -U {user} -p {port} {name} -w"\
            .format(
                host = self.host, user = self.user, port = self.port,
                name = self.db_name)

    def __create_db(self):
        self.__collorg_db.close()
        self.__create_cog_ini_file()
        exit_status = os.system(
            "export PGPASSWORD={password};"
            "createdb {db_name} -O {user} -U {user} "
            "-T collorg_db -h {host}".format(
                password = self.password, db_name = self.db_name,
                user = self.user, host = self.host))
        if exit_status != 0:
            sys.stderr.write("unable to create database %s\n%s\n" % (
                self.db_name, exit_status))
            sys.exit(exit_status)

    def __create_cog_ini_file(self):
        try:
            open("/etc/collorg/%s" % (self.db_name))
            return
        except:
            pass
        file_ = app_ini_file.format(
            user = self.user, password = self.password,
            host = self.host, port = self.port,
            charset = self.charset, db_name = self.db_name)
        os.popen('sudo su - -c "cat>/etc/collorg/{}<<EOF\n{}\nEOF\n"'.format(
            self.db_name, file_))

    def __make_cog_repos(self):
        db_name = self.db.name
        base_dir = "%s/%s" % (self.__curdir, db_name)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
            open("%s/__init__.py" % (base_dir), "w")
            if not os.path.exists("%s/.cog" % (base_dir)):
                os.mkdir("%s/.cog" % (base_dir))
                open("%s/.cog/config" % (base_dir), "w").write(
                    cog_config_file % (db_name))
        os.chdir(base_dir)
        self.abs_base_dir = os.path.abspath(os.path.curdir)
        sys.path.insert(0, self.abs_base_dir)
        cog_app_pkg_dir = "%s" % (glob.cog_pkg_path(self.db_name))
        if not os.path.exists(cog_app_pkg_dir):
            os.makedirs(cog_app_pkg_dir)
            for dir_ in ("../..", "..", "."):
                open("%s/%s/__init__.py" % (cog_app_pkg_dir, dir_), "w")
        open("%s/__init__.py" % (cog_app_pkg_dir), "w")
        os.chdir(cog_app_pkg_dir)
        self.post_init()

    def add_user(self):
        db = self.db
        user = db.table('collorg.actor.user')
        kwargs = {}
        kwargs['first_name_'] = raw_input('First name: ')
        kwargs['last_name_'] = raw_input('Last name: ')
        kwargs['email_'] = raw_input('email: ')
        kwargs['pseudo_'] = raw_input('pseudo: ')
        pass1 = ''
        pass2 = 'x'
        while pass1 != pass2:
            pass1 = getpass.getpass('password: ')
            pass2 = getpass.getpass('password (retype): ')
            if pass1 == pass2:
                if pass1 == '':
                    print("Empty password. aborting!")
                    sys.exit()
                break
            else:
                print("password mismatch!")
        kwargs['password_'] = pass1
        user.new_account(**kwargs)
        return user.get()

    def __make_dirs(self):
        os.chdir(self.abs_base_dir)
        app_base_dir = self.db._cog_params['application_basedir']
        setup = open("{}/examples/setup.py".format(app_base_dir)).read()
        setup = setup.replace('__DB_NAME__', self.db_name)
        makefile = open("{}/examples/Makefile".format(app_base_dir)).read()
        makefile = makefile.replace('__DB_NAME__', self.db_name)
        os.mkdir('sql')
        os.mkdir('scripts')
        open("setup.py", "w").write(setup)
        open("Makefile", "w").write(makefile)

        document_root = self.db._cog_params['document_root']
        apache_user = "www-data"
        os.system("sudo mkdir {}".format(document_root))
        os.system("sudo mkdir {}/download".format(document_root))
        os.system("sudo chown -R {}:{} {}".format(
            apache_user, apache_user, document_root))
        os.system("sudo chmod -R 700 {}".format(document_root))

        upload_dir = self.db._cog_params['upload_dir']
        os.system("sudo mkdir {}".format(upload_dir))
        os.system("sudo mkdir {}/tmp".format(upload_dir))
        os.system("sudo mkdir {}/uploaded_files".format(upload_dir))
        os.system("sudo chown -R {}:{} {}".format(
            apache_user, apache_user, upload_dir))
        os.system("sudo chmod -R 700 {}".format(upload_dir))

    def post_init(self):
        self.__make_dirs()

        table = self.db.table
        #db.set_auto_commit(False)
        user = self.add_user()
        assert user.count() == 1
        db = table('collorg.core.database').get()
        ndb = db()
        ndb.name_.set_intention(self.db.name)
        db.update(ndb)
        site = table('collorg.web.site')
        site.url_.set_intention('{}/collorg'.format(self.db.name))
        if not site.exists():
            site.insert()
        assert site.count() == 1
        unit = table('collorg.organization.unit')
        unit.acronym_.set_intention('Collorg')
        unit.name_.set_intention('Collorg unit')
        unit.cog_fqtn_.set_intention('collorg.organization.unit')
        if not unit.exists():
            unit.insert()
        assert unit.count() == 1
        topic = table('collorg.web.topic')
        topic._site_ = site
        topic._author_ = user
        topic._cog_environment_ = unit
        topic.title_.set_intention('Home')
        topic.path_info_.set_intention('/')
        topic.author_.set_intention(user.cog_oid_.value)
        if not topic.exists():
            topic.insert()
        assert topic.count() == 1
        topic.get()
        user.grant_access(unit, True)
        user.grant_access(topic, True)
        #db.commit()
