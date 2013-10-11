#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, sys
import argparse
import hashlib
from collorg.controller.controller import Controller
from collorg.templates.parser import Parser
import collorg.utils.globvars as glob
from _utils.system_users import System_users
from _utils.gen_relational_part import GenRelationalPart
from _utils.make_site import Make_site
from _utils.action_requirement import Action_requirement

class Cmd():
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.db = self.__ctrl.db
        self.__db_name = self.db.name
        self.__collorg_db = None
        if self.__db_name != 'collorg_db':
            self.__collorg_db_ctrl = Controller('collorg_db')
            self.__collorg_db = self.__collorg_db_ctrl.db
        self.pkg_path = glob.cog_pkg_path(self.db.name)
        self.mod_path = self.pkg_path.replace("/", ".")
        self.__repos_base_dir = self.__ctrl.repos_path
        sys.path.insert(0, self.__repos_base_dir)
        sys.path.insert(0, ".")
        self.__rerun = False
        self.__parse_args()
        #XXX recopie brute de collorg.utils.make.py # REMOVE ME WHEN DONE
        self.template_module = None
        self.l_schemas = [ self.mod_path ]
        self.db = Controller(self.db.name).db
        self.db.table('collorg.core.data_type')._populate()
        self.charset = self.db._cog_controller._charset
        System_users(self.__ctrl).check()
        self.make_cog_tree()
        cog_table = self.db.table('collorg.core.data_type')
        for fqtn in self.db.fqtns:
            cog_table = self.db.table('collorg.core.data_type')
            cog_table.fqtn_.set_intention(fqtn)
            tablename = fqtn.rsplit('.', 1)[1]
            cog_table.name_.set_intention(tablename)
            if not cog_table.count():
                cog_table.insert()
        self.__gen_templates()
        GenRelationalPart(self.__ctrl)
        Make_site(self.__ctrl)
        os.system(
            "cd %s;make clean_install > /dev/null"
            ";sudo python setup.py -q install" % (
                self.__repos_base_dir))
#        os.system("sudo service apache2 restart")
        if self.__rerun:
            os.system("cog make")
#            print("Please rerun cog make to finish install.")
        Action_requirement(self.__ctrl).update_check()
        os.system("sudo service apache2 restart")

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog make")
        parser.add_argument(
            "-a", "--an_arg", help = "an argument", required = False)
        self.__args = parser.parse_args()

    def __get_pkg_path(self, pkg_path):
        if pkg_path.find("collorg/") == 0 and self.db.name == 'collorg_db':
            pkg_path = pkg_path.replace('collorg/', '')
        return pkg_path

    def make_cog_tree(self):
        cog_app_pkg_dir = "%s/%s" % (self.__repos_base_dir, self.pkg_path)
        if not os.path.exists(cog_app_pkg_dir):
            os.makedirs(cog_app_pkg_dir)
            the_dir = self.__repos_base_dir
            for dir_ in self.pkg_path.split('/'):
                the_dir = "%s/%s" % (the_dir, dir_)
                open("%s/__init__.py" % the_dir, "w")
        for schema in self.db.schemas:
            os.chdir(cog_app_pkg_dir)
            if schema.name.find("collorg.") == 0 and self.db.name != 'collorg_db':
                continue
            self.l_schemas.append("%s.%s" % (self.mod_path, schema.name))
            self.l_schemas.append("%s.%s.%s" % (
                    self.mod_path, schema.name, glob.templates_dir))
            pkg_path = self.__get_pkg_path(schema.name.replace(".", "/"))
            if not os.path.exists(pkg_path):
                os.makedirs(pkg_path)
                open("%s/__init__.py" % (pkg_path), "w")
            os.chdir(pkg_path)
            for tablename in schema.tables:
                fqtn = "%s.%s" % (schema.name, tablename)
                module = self.db.table(
                    'collorg.core.data_type', fqtn_ = fqtn, name_ = tablename)
                if not module.exists():
                    module.insert()
                if not os.path.exists("%s/__init__.py" % (tablename)):
                    print("+ adding package %s.%s" % (schema.name, tablename))
                    os.makedirs("%s/%s/__src" % (
                        tablename, glob.templates_dir))
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
                    open("%s/%s/__src/.readme" % (
                            tablename, glob.templates_dir), "w")
                self.l_schemas.append(
                    "%s.%s.%s.%s" % (
                        self.mod_path,
                        schema.name, tablename, glob.templates_dir))
        os.chdir(self.__repos_base_dir)
        if not os.path.exists("setup.py"):
            fd = open("setup.py", "w")
            fd.write(glob.setup_template % (self.db.name))
            fd.close()

    def __get_templates(self, path):
        l_templates = []
        try:
            l_files = os.listdir(path)
        except:
            # first time. the path doesn't exist
            return l_templates
        for file_ in l_files:
            if file_.find('__init__') == 0 or file_.find('.pyc') != -1:
                continue
            l_templates.append(file_.replace('.py', ''))
        return l_templates

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

    def __treat_pragmas(self, action):
        """
        before saving action
        """
#        template_module = ".".join(self.template_module.split(".")[:-1])
        task = None
        try:
            module = __import__(
                self.template_module, globals(), locals(), [action.name_], -1)
        except:
            # the module is not installed yet. cog make is to be run again
#            print("Unable to load %s. Please, rerun cog make." %
#                self.template_module)
            self.__rerun = True
            print("ERR", self.template_module)
            return
        if hasattr(module, 'PRAGMA'):
            PRAGMA = module.PRAGMA
            goals = PRAGMA.get('goals', [])
            assert type(goals) is list
            tasks = PRAGMA.get('tasks', [])
            assert type(tasks) is list
#            if not tasks:
#                print("Warning! No task defined.")
            functions = PRAGMA.get('functions', [])
#            if not functions:
#                print("Warning! No function defined.")
            assert type(functions) is list
            attrs = [
                'description', 'label', 'icon',
                'in_menu', 'in_header', 'in_nav',
                'raw',
                #XXX TODO
                'write', 'moderate', 'admin']
            for attr in attrs:
                if attr in PRAGMA.keys():
                    action.__dict__["%s_" % attr].set_intention(PRAGMA[attr])
            action.insert()
            if not tasks and not functions:
                print("Linking action to 'Anonymous navigation'")
                task = self.db.table(
                    'collorg.application.task', name_ = 'Anonymous navigation')
                aat = task._rev_a_action_task_
                aat._action_ = action
                if not aat.exists():
                    aat.insert()
            for goal_ in goals:
                for task_ in tasks:
                    goal = self.db.table(
                        'collorg.application.goal', name_=goal_)
                    task = self.db.table(
                        'collorg.application.task', name_=task_)
                    if not goal.exists():
                        print("+ new goal %s" % (goal.name_.val))
                        goal.insert()
                    if not task.exists():
                        print("+ new task %s" % (task.name_.val))
                        task.insert()
                    atg = task._rev_a_task_goal_
                    atg._goal_ = goal
                    if not atg.exists():
                        atg.insert()
                    try:
                        action.link_to_task(task)
                    except:
                        print("ERR! could not link action to task")
            for task_ in tasks:
                task = self.db.table(
                    'collorg.application.task', name_=task_)
                if not task.exists():
                    print("+ new task %s" % (task.name_.val))
                    task.insert()
                for function_ in functions:
                    function = self.db.table(
                        'collorg.actor.function', long_name_=function_)
                    atf = task._rev_a_task_function_
                    atf._function_ = function
                    if not atf.exists():
                        print("+ task<->function: %s<->%s" % (
                            task.name_, function.long_name_))
                        atf.insert()
                aat = task._rev_a_action_task_
                aat._action_ = action
                if not aat.exists():
                    aat.insert()

    def __set_template_module_string(
        self, schemaname, tablename, template_name):
            if (self.db.name == 'collorg_db' or (
                self.this_application and schemaname.find('collorg.') == 0)):
                    schemaname = schemaname.replace('collorg.', '')
                    self.template_module = \
                        "collorg.db.{}.{}.cog.templates.{}".format(
                            schemaname, tablename, template_name)
            else:
                self.template_module = "%s.%s.%s.cog.templates.%s" % (
                    self.mod_path, schemaname, tablename, template_name)

    def __add_action(self, schemaname, tablename, tsn, template_code = None):
        # ajout action
        self.__set_template_module_string(schemaname, tablename, tsn)
        fqtn = "%s.%s" % (schemaname, tablename)
        module = self.db.table(
            'collorg.core.data_type', fqtn_ = fqtn)
        if not module.exists():
            module.insert()
        action = self.db.table('collorg.application.action', name_ = tsn)
        action._data_type_ = module
        if not action.exists():
            print("+ new action %s.%s %s" % (schemaname, tablename, tsn))
            action.source_.set_intention(template_code)
            self.__treat_pragmas(action)

    def __remove_cog_templates(self):
        """
        For each action in the database, check if the source is still
        here and removes it from the database if not.
        """
        import collorg
        cog_base_dir = collorg.__path__[0]
        cog_app_pkg_dir = "{}/{}".format(self.__repos_base_dir, self.pkg_path)
        action = self.db.table('collorg.application.action')
        action.this_application_.set_intention(True)
        for act in action:
            missing = False
            data_type = act.data_type_.value
            data_type_path = self.__get_pkg_path(
                data_type.replace('.', '/'))
            src_path = "{}/{}/cog/templates/__src/{}".format(
                cog_app_pkg_dir, data_type_path, act.name_)
            if((data_type.find("collorg.") == 0 and
                self.db.name == "collorg_db") or
               (data_type.find("collorg.") == -1 and
                self.db.name != "collorg_db")):
                if not os.path.exists(src_path):
                    print("MISSING: {}".format(src_path))
                    missing = True
            elif((data_type.find("collorg.") == 0 and
                self.db.name != "collorg_db")):
                act_cog = self.__collorg_db.table('collorg.application.action')
                act_cog.name_.set_intention(act.name_.value)
                act_cog.data_type_.set_intention(data_type)
                if not act_cog.exists():
                    print("MISSING: {}, {}".format(data_type, act.name_))
                    missing = True
            if missing:
                module_path = [
                    "{}/{}/cog/templates/{}".format(
                        cog_app_pkg_dir, data_type_path, act.name_),
                    "{}/db/{}/cog/templates/{}*".format(
                    cog_base_dir, data_type_path, act.name_),
                    "{}/build/*/db/{}/cog/templates/{}".format(
                        self.__repos_base_dir, data_type_path, act.name_)]
                for mp in module_path:
                    for ext in ["py", "pyc", "pyo"]:
                        file_ = "{}.{}".format(mp, ext)
                        if os.path.exists(file_):
                            os.popen("sudo rm -f {}".format(file_))
                            print("-{}".format(file_))
                act._rev_a_action_task_.delete()
                act.delete()
                print("- action removed")

    def __add_cog_templates(self):
        cog_base_dir = "{}/{}".format(self.__repos_base_dir, self.pkg_path)
        if self.db.name != 'collorg_db':
            import collorg
            cog_base_dir = collorg.__path__[0]
        for schema in self.db.schemas:
            if schema.name.find("collorg.") != 0:
                continue
            schemaname = schema.name.replace('collorg.', '')
            for tablename in schema.tables:
                path = "%s/db/%s/%s/cog/templates/" % (
                        (cog_base_dir,
                          schemaname.replace(".", "/"),
                          tablename))
                if os.path.exists(path):
                    for template_name in self.__get_templates(path):
                        self.__add_action(
                            schema.name, tablename, template_name)

    def __gen_templates(self):
        """
        Check les rép. <db>/<schema>/<module>/cog/templates/__src/<fichier>
        Parse chaque fichier et génère un module "<fichier>.py" dans le rép.
        <db>/<schema>/cog/templates/<module>/.
        Insert dans la table action la réf. à la template
        """
        self.this_application = True
        self.__remove_cog_templates()
        self.__add_cog_templates()
        cog_app_pkg_dir = "%s/%s" % (self.__repos_base_dir, self.pkg_path)
        for schema in self.db.schemas:
            os.chdir(cog_app_pkg_dir)
            schema_path = schema.name.replace(".", "/")
            if self.db.name == 'collorg_db':
                schema_path = schema_path.replace("collorg/", "")
            if not os.path.exists(schema_path):
                continue
            os.chdir(schema_path)
            for tablename in schema.tables:
                # parcours du rép. cog/templates/__src/<tablename>
                path = "%s/%s/__src" % (tablename, glob.templates_dir)
                init_content = []
                init_file = "%s/%s/__init__.py" % (
                    tablename, glob.templates_dir)
                for template_src_name in self.__get_templates(path):
                    parser = Parser()
                    tsn = template_src_name
                    if not((tsn[0].isalpha() or tsn[0] == '_') and
                            (tsn[1:].replace('_', '').isalnum())):
                        continue
                    src_file = "%s/%s/__src/%s" % (
                        tablename, glob.templates_dir, tsn)
                    template_src = open(src_file).read()
                    template_code = parser.parse(
                        tsn, template_src,
                        "%s/%s/%s/%s/__src/%s" % (
                            self.pkg_path, schema.name,
                            tablename, glob.templates_dir, tsn))
                    template_sha = hashlib.sha1(
                        template_code).hexdigest()
                    template_module_name = "%s/%s/%s.py" % (
                        tablename, glob.templates_dir, tsn)
                    self.this_application = True
                    if (self.db.name != 'collorg_db' and
                        schema.name.find('collorg.') == 0):
                            self.this_application = False
                    module_sha = None
                    if os.path.exists(template_module_name):
                        module_sha = hashlib.sha1(
                            open(template_module_name).read()).hexdigest()
                    if template_sha != module_sha:
                        print("+ template modified: %s" % (src_file))
                        fd = open(template_module_name, "w")
                        fd.write(template_code)
                        fd.close()
                    self.__add_action(
                        schema.name, tablename, tsn, template_src)
                    init_content.append(tsn)
                try:
                    init_content.sort()
                    open(init_file, "w").write("__all__ = [{}]".format(
                        ", ".join(
                            ['"{}"'.format(elt) for elt in init_content])))
                except:
                    pass
                    #print("ERROR gen init templates file {} for {} {}".format(
                    #    init_file, schema.name, tablename))
        os.chdir(self.__repos_base_dir)

