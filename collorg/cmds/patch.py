#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, sys
import argparse
import ConfigParser
import subprocess
from collorg.controller.controller import Controller
import collorg.utils.globvars as glob
from ._utils.gen_relational_part import GenRelationalPart
from .make import Cmd as Make

help_ = """
revision is <major>.<minor>.<revision> and references
a patch located in <collorg app dir>/<major>/<minor>/<revision>.

The patch is composed of an ini file patch.ini
"""


class Cmd():
    global help_
    __known_items = [
        'stage',
        'label', 'description',
        'tickets',
        'pre', 'sql', 'post']
    __stages = ['alpha', 'beta', 'candidate', 'release', 'unsupported']
    cmd_help = (help_)
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.db = self.__ctrl.db
        self.__database = self.db.table('collorg.core.database')
        self.__db_name = self.db.name
        self.__database.name_.value = self.__db_name
        assert self.__database.count() == 1
        self.__patch = None
        self.__patch_dir = None
        self.__major = None
        self.__minor = None
        self.__revision = None
        self.__cfg_file = None
        self.__output = []
        self.__error = []
        self.pkg_path = glob.cog_pkg_path(self.db.name)
        self.mod_path = self.pkg_path.replace("/", ".")
        self.__repos_base_dir = self.__ctrl.repos_path
        self.__parse_args()
        self.__execute()

    def reload_db(self):
        self.__ctrl = Controller()
        self.db = self.__ctrl.db

    def __check_revision(self):
        """
        We will check here if the patch can be applied...
        """
        # the revision must be greater than the already applied patches
        # TODO
        # is the patch config file accessible
        self.__patch_dir = "%s/patches/%s/%s/%s" % (
            self.db._cog_params['application_basedir'],
            self.__major, self.__minor, self.__revision)
        self.__cfg_file = "%s/patch.cfg" % (self.__patch_dir)
        # all the files mentioned in the ini file must be accessible
        self.__config.read(self.__cfg_file)
        self.__items = {}
        if not self.__config.has_section('patch'):
            sys.stderr.write(
                "No section: patch in patch.cfg\n"
                "Have you run 'python setup.py install'?\n")
            sys.exit()
        for key, val in self.__config.items('patch'):
            self.__items[key] = val[1:].strip()
        assert self.__items['stage'] in self.__stages
        assert 'label' in self.__items
        assert 'description' in self.__items
        for key, val in self.__items.items():
            if key not in self.__known_items:
                raise ValueError("Unknown item: %s" % key)

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog patch")
        parser.add_argument(
            "-r", "--revision", help = self.cmd_help, required = True)
        self.__args = parser.parse_args()
        self.__config = ConfigParser.ConfigParser()
        self.__major, self.__minor, self.__revision = \
            self.__args.revision.split('.')
        self.__check_revision()
        os.path.abspath(os.path.dirname(self.__cfg_file))
        sys.argv = []

    def __execute(self):
        for section in self.__config.sections():
            if section == 'patch':
                patch_res = self.__ex_patch()
                GenRelationalPart(self.__ctrl)
                return patch_res
        print("nothing")

    def __ex_patch(self):
        if 'pre' in self.__items:
            self.__pre_patch(self.__items['pre'])
        self.__patch = self.db.table("collorg.core.patch.changelog")
        self.__patch.major_.value = self.__major
        self.__patch.minor_.value = self.__minor
        self.__patch.revision_.value = self.__revision
        if self.__patch.count() == 1:
            sys.exit("Patch already applied\n")
        self.__patch._database_ = self.__database
        self.__patch.stage_.value = \
            self.__stages.index(self.__items['stage'])
        self.__patch.label_.value = self.__items['label']
        self.__patch.description_.value = \
            self.__items['description']
        if 'sql' in self.__items:
            self.__sql_patch(self.__items['sql'])
        if 'post' in self.__items:
            self.__post_patch(self.__items['post'])
        self.__patch.error_.value = "\n".join(self.__error)
        self.__patch.output_.value = "\n".join(self.__output)
        if self.__patch is not None:
            self.__patch.insert()

    def __pre_patch(self, items):
        print("Pre patch")
        for item in items.split('\n'):
            print(item)
            sp = subprocess.Popen(
                ["%s/%s" % (self.__patch_dir, item), self.db.name])
            return_code = sp.wait()
            out, err = sp.communicate()
            self.__output.append("==%s==\n%s" % (item, out))
            if err:
                self.__error.append("==%s==\n%s" % (item, err))
            if return_code != 0:
                print("+++%s---" % return_code)
                raise RuntimeError("%s\n%s\nErr: %s" % (item, out, err))
        self.reload_db()

    def __sql_patch(self, items):
        print("SQL patch")
        for item in items.split('\n'):
            if item[0] == '#':
                continue
            print(item)
            sql_file = "%s/%s" % (self.__patch_dir, item)
            os.system("psql %s -f %s" % (self.db.name, sql_file))
        self.reload_db()
        self.__add_missing_modules()

    def __post_patch(self, items):
        print("Post patch")
        for item in items.strip().split('\n'):
            print(item)
            os.system("%s/%s" % (self.__patch_dir, item))

    def __get_inh_infos(self, fqtn):
        # héritage sql
        import_line = "from %s import %s"
        l_imports = []
        l_class_names = []
        inh_fqtns = self.db._sql_inherits(fqtn)
        for fqtn in inh_fqtns:
            module_path = fqtn
            class_name = fqtn.split('.')[-1].capitalize()
            if fqtn.find('collorg.') == 0:
                module_path = fqtn.replace('collorg.', 'collorg.db.')
            else:
                module_path = "%s.%s" % (self.mod_path, fqtn)
            l_imports.append(import_line % (module_path, class_name))
            l_class_names.append(class_name)
        if not l_imports:
            l_imports.append("from collorg.orm.table import Table")
            l_class_names.append("Table")
        return ", ".join(l_class_names), "\n".join(l_imports)

    def __add_missing_modules(self):
        self.db = Controller().db
        for fqtn in self.db.fqtns:
            cog_table = self.db.table('collorg.core.data_type')
            cog_table.fqtn_.value = fqtn
            tablename = fqtn.rsplit('.', 1)[1]
            cog_table.name_.value = tablename
            if not cog_table.count():
                print("+ adding table %s to data_type" % fqtn)
                cog_table.insert()
        sys.path.insert(0, self.__repos_base_dir)
        cog_app_pkg_dir = "%s/%s" % (self.__repos_base_dir, self.pkg_path)
        if not os.path.exists(cog_app_pkg_dir):
            os.makedirs(cog_app_pkg_dir)
        open("%s/__init__.py" % (cog_app_pkg_dir), "w")
        for schema in self.db.schemas:
            if (schema.name.find("collorg.") == 0 and
                self.db.name != 'collorg_db'):
                continue
            os.chdir(cog_app_pkg_dir)
            schema_path = schema.name.replace(".", "/")
            if schema_path.find("collorg/") == 0:
                schema_path = schema_path.replace("collorg/", "")
            if not os.path.exists(schema_path):
                print("+ new schema: %s" % schema_path)
                os.makedirs(schema_path)
                open("%s/__init__.py" % (schema_path), "w")
            os.chdir(schema_path)
            for tablename in schema.tables:
                fqtn = "%s.%s" % (schema.name, tablename)
                module = self.db.table(
                    'collorg.core.data_type', fqtn_ = fqtn, name_ = tablename)
                if module.is_empty():
                    module.insert()
                if not os.path.exists("%s/__init__.py" % (tablename)):
                    print("+ adding package %s.%s" % (schema.name, tablename))
                    fd = open("%s/__init__.py" % (tablename), "w")
                    inh_classes, import_statment = self.__get_inh_infos(fqtn)
                    fd.write(glob.module_template % (
                        self.__ctrl._charset,
                        import_statment,
                        tablename.capitalize(),
                        inh_classes,
                        schema.name, tablename,
                        tablename.capitalize()))
                    fd.close()
                    open("%s/cog/__init__.py" % (tablename), "w")
                    open("%s/%s/__init__.py" % (
                            tablename, glob.templates_dir), "w")
        Make(self.__ctrl, self.__db_name)
