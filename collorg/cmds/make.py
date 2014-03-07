#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
cog command invoqued by: cog make.
"""

import os, sys
import argparse
import hashlib
from collorg.controller.controller import Controller
from collorg.templates.parser import Parser
import collorg.utils.globvars as glob
from _utils.system_users import System_users
from _utils.gen_relational_part import GenRelationalPart
from _utils.action_requirement import Action_requirement

class Cmd():
    """
    * Generates the code to handle new tables in the database.
    * Generates the templates modules when cog templates are modified or
      created
    """
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.db_ = self.__ctrl.db
        self.__db_name = self.db_.name
        self.__collorg_db = None
        if self.__db_name != 'collorg_db':
            self.__collorg_db_ctrl = Controller('collorg_db')
            self.__collorg_db = self.__collorg_db_ctrl.db
        self.pkg_path = glob.cog_pkg_path(self.db_.name)
        self.mod_path = self.pkg_path.replace("/", ".")
        self.__repos_base_dir = self.__ctrl.repos_path
        sys.path.insert(0, self.__repos_base_dir)
        sys.path.insert(0, ".")
        self.__rerun = 0
        self.__parse_args()
        #XXX recopie brute de collorg.utils.make.py # REMOVE ME WHEN DONE
        self.template_module = None
        self.l_schemas = [ self.mod_path ]
        self.db_ = Controller(self.db_.name).db
        self.db_.table('collorg.core.data_type')._populate()
        self.charset = self.db_._cog_controller._charset
        System_users(self.__ctrl).check()
        self.make_cog_tree()
        cog_table = self.db_.table('collorg.core.data_type')
        for fqtn in self.db_.fqtns:
            cog_table = self.db_.table('collorg.core.data_type')
            cog_table.fqtn_.value = fqtn
            tablename = fqtn.rsplit('.', 1)[1]
            cog_table.name_.value = tablename
            if not cog_table.count():
                cog_table.insert()
        self.__gen_templates()
        GenRelationalPart(self.__ctrl)
        os.system(
            "cd {};make clean_install > /dev/null"
            ";sudo python setup.py -q install".format(
                self.__repos_base_dir))
#        os.system("sudo service apache2 restart")
        if self.__rerun and self.__rerun < 2:
            os.system("cog make")
#            print("Please rerun cog make to finish install.")
        if self.db_.name != 'collorg_db':
            self.__sync_collorg_actions()
        Action_requirement(self.__ctrl).update_check()
        os.system("sudo service apache2 restart")

    def __dup_task(self, task_to_dup, duped_task):
        """
        duplicates task_to_dup which is the result of a .get leaving
        the cog_* fields at None into duped_task.
        """
        t2d = task_to_dup
        dt_ = duped_task
        dt_.name_.value = t2d.name_.value
        dt_.delegable_.value = t2d.delegable_.value
        dt_.description_.value = t2d.description_.value
        return dt_

    def __dup_action(self, action_to_dup, duped_action):
        """
        action_to_dup is the action to duplicate. duped_action is the
        returned duplicated action
        """
        da_ = duped_action
        a2d = action_to_dup
        da_.data_type_.value = a2d.data_type_.value
        da_.name_.value = a2d.name_.value
        da_.label_.value = a2d.label_.value
        da_.description_.value = a2d.description_.value
        da_.format_.value = a2d.format_.value
        da_.source_.value = a2d.source_.value
        da_.raw_.value = a2d.raw_.value
        da_.protected_.value = a2d.protected_.value
        da_.in_menu_.value = a2d.in_menu_.value
        da_.in_header_.value = a2d.in_header_.value
        da_.in_nav_.value = a2d.in_nav_.value
        da_.write_.value = a2d.write_.value
        da_.moderate_.value = a2d.moderate_.value
        da_.admin_.value = a2d.admin_.value
        da_.icon_.value = a2d.icon_.value
        return da_

    def __sync_collorg_actions(self):
        """
        Synchonize application actions with collorg reference database.
        1. remove removed collorg actions
        2. add missing collorg actions
        """
        aa_ = self.db_.table('collorg.application.action')
        ca_ = self.__collorg_db.table('collorg.application.action')
        for action in aa_:
            sca = ca_()
            sca.data_type_.value = ca_.data_type_.value
            sca.name_.value = ca_.name_.value
            if sca.is_empty():
                print("- {}.{} missing".format(ca_.data_type_, ca_.name_))
                rat = action._rev_a_action_task_
                if not rat.is_empty():
                    rat.delete()
                action.delete()
        for action in ca_():
            aa_ = self.__dup_action(action, aa_())
            tasks = action._rev_a_action_task_._task_
            saa = aa_()
            saa.data_type_.value = aa_.data_type_.value
            saa.name_.value = aa_.name_.value
            if saa.is_empty():
                print("++ action {}.{}".format(aa_.data_type_, aa_.name_))
                aa_.insert()
                aa_.get()
                for task in tasks:
                    ta_ = self.db_.table('collorg.application.task')
                    ta_.name_.value = task.name_.value
                    if ta_.is_empty():
                        # XXX  mettre une méthode pour faire ce qui suit
                        ta_.delegable_.value = task.delegable_.value
                        ta_.description_.value = task.description_.value
                        ta_.insert()
                        orig_goal = task._rev_a_task_goal_._goal_
                        if not orig_goal.is_empty():
                            orig_goal.get()
                            goal = self.db_.table('collorg.application.goal')
                            goal.name_.value = orig_goal.name_.value
                            goal.insert()
                            atg = goal._rev_a_task_goal_
                            atg._task_ = ta_
                            atg.insert()
                        orig_function = task._rev_a_task_function_._function_
                        orig_function.get()
                        function = self.db_.table('collorg.actor.function')
                        function.name_.value = orig_function.name_.value
                        if function.is_empty():
                            function.fname_.value = orig_function.fname_.value
                            function.long_name_.value = \
                                orig_function.long_name_.value
                            function.advertise_.value = \
                                orig_function.advertise_.value
                            # XXX check if data_type exists
                            function.data_type_.value = \
                                orig_function.data_type_.value
                            function.insert()
                        atf = function._rev_a_task_function_
                        atf._task_ = ta_
                        atf.insert()
                    ta_.get()
                    aat = aa_._rev_a_action_task_
                    aat._task_ = ta_
                    print("++ link to task {}".format(task.name_))
                    aat.insert()
                    aat.get()
            else:
                saa.update(aa_)

    def __parse_args(self):
        """arguments parser"""
        parser = argparse.ArgumentParser(prog="cog make")
        parser.add_argument(
            "-a", "--an_arg", help = "an argument", required = False)
        self.__args = parser.parse_args()

    def __get_pkg_path(self, pkg_path):
        """returns package path according to the collorg convention"""
        if pkg_path.find("collorg/") == 0 and self.db_.name == 'collorg_db':
            pkg_path = pkg_path.replace('collorg/', '')
        return pkg_path

    def make_cog_tree(self):
        """
        Constructs the collorg tree when new tables are created in the
        database.
        """
        cog_app_pkg_dir = "{}/{}".format(self.__repos_base_dir, self.pkg_path)
        if not os.path.exists(cog_app_pkg_dir):
            os.makedirs(cog_app_pkg_dir)
            the_dir = self.__repos_base_dir
            for dir_ in self.pkg_path.split('/'):
                the_dir = "{}/{}".format(the_dir, dir_)
                open("{}/__init__.py".format(the_dir), "w")
        for schema in self.db_.schemas:
            os.chdir(cog_app_pkg_dir)
            if (schema.name.find("collorg.") == 0 and
            self.db_.name != 'collorg_db'):
                continue
            self.l_schemas.append("{}.{}".format(self.mod_path, schema.name))
            self.l_schemas.append("{}.{}.{}".format(
                    self.mod_path, schema.name, glob.templates_dir))
            pkg_path = self.__get_pkg_path(schema.name.replace(".", "/"))
            if not os.path.exists(pkg_path):
                os.makedirs(pkg_path)
                open("{}/__init__.py".format(pkg_path), "w")
            os.chdir(pkg_path)
            for tablename in schema.tables:
                fqtn = "{}.{}".format(schema.name, tablename)
                module = self.db_.table(
                    'collorg.core.data_type', fqtn_ = fqtn, name_ = tablename)
                if module.is_empty():
                    module.insert()
                if not os.path.exists("{}/__init__.py".format(tablename)):
                    print("+ adding package {}.{}".format(
                        schema.name, tablename))
                    os.makedirs("{}/{}".format(tablename, glob.templates_dir))
                    fd_ = open("{}/__init__.py".format(tablename), "w")
                    inh_classes, import_statment = self.__get_inh_infos(fqtn)
                    fd_.write(glob.module_template.format(
                        self.__ctrl._charset,
                        import_statment,
                        tablename.capitalize(),
                        inh_classes,
                        schema.name, tablename,
                        tablename.capitalize()))
                    fd_.close()
                    open("{}/cog/__init__.py".format(tablename), "w")
                    open("{}/{}/__init__.py".format(
                            tablename, glob.templates_dir), "w")
                self.l_schemas.append(
                    "{}.{}.{}.{}".format(
                        self.mod_path,
                        schema.name, tablename, glob.templates_dir))
        os.chdir(self.__repos_base_dir)
        if not os.path.exists("setup.py"):
            fd_ = open("setup.py", "w")
            fd_.write(glob.setup_template.format(self.db_.name))
            fd_.close()

    def __get_inh_infos(self, fqtn):
        """return the list of inherited classes"""
        import_line = "from {} import {}"
        l_imports = []
        l_class_names = []
        inh_fqtns = self.db_._sql_inherits(fqtn)
        for fqtn in inh_fqtns:
            module_path = fqtn
            class_name = fqtn.split('.')[-1].capitalize()
            if fqtn.find('collorg.') == 0:
                module_path = fqtn.replace('collorg.', 'collorg.db.')
            else:
                module_path = "{}.{}".format(self.mod_path, fqtn)
            l_imports.append(import_line.format(module_path, class_name))
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
            print("Unable to load {}. Please, rerun cog make.".format(
                self.template_module))
            self.__rerun += 1
            print("ERR", self.template_module)
            return
        if hasattr(module, 'PRAGMA'):
            pragma = module.PRAGMA
            goals = pragma.get('goals', [])
            assert type(goals) is list
            tasks = pragma.get('tasks', [])
            assert type(tasks) is list
#            if not tasks:
#                print("Warning! No task defined.")
            functions = pragma.get('functions', [])
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
                if attr in pragma:
                    action.__dict__["{}_".format(attr)].value = pragma[attr]
            action.insert()
            if not tasks and not functions:
                print("Linking action to 'Anonymous navigation'")
                task = self.db_.table(
                    'collorg.application.task', name_ = 'Anonymous navigation')
                aat = task._rev_a_action_task_
                aat._action_ = action
                if aat.is_empty():
                    aat.insert()
            for goal_ in goals:
                for task_ in tasks:
                    goal = self.db_.table(
                        'collorg.application.goal', name_=goal_)
                    task = self.db_.table(
                        'collorg.application.task', name_=task_)
                    if goal.is_empty():
                        print("+ new goal {}".format(goal.name_.value))
                        goal.insert()
                    if task.is_empty():
                        print("+ new task {}".format(task.name_.value))
                        task.insert()
                    atg = task._rev_a_task_goal_
                    atg._goal_ = goal
                    if atg.is_empty():
                        atg.insert()
                    try:
                        action.link_to_task(task)
                    except:
                        print("ERR! could not link action to task")
            for task_ in tasks:
                task = self.db_.table(
                    'collorg.application.task', name_=task_)
                if task.is_empty():
                    print("+ new task {}".format(task.name_.value))
                    task.insert()
                for function_ in functions:
                    function = self.db_.table(
                        'collorg.actor.function', long_name_=function_)
                    atf = task._rev_a_task_function_
                    atf._function_ = function
                    if atf.is_empty():
                        print("+ task<->function: {}<->{}".format(
                            task.name_, function.long_name_))
                        atf.insert()
                aat = task._rev_a_action_task_
                aat._action_ = action
                if aat.is_empty():
                    aat.insert()

    def __set_template_module_string(
    self, schemaname, tablename, template_name):
        """
        returns the template module string according to the collorg
        source tree organization.
        """
        if (self.db_.name == 'collorg_db' or (
        self.this_application and schemaname.find('collorg.') == 0)):
            schemaname = schemaname.replace('collorg.', '')
            self.template_module = \
                "collorg.db.{}.{}.templates.{}".format(
                    schemaname, tablename, template_name)
        else:
            self.template_module = "{}.{}.{}.templates.{}".format(
                self.mod_path, schemaname, tablename, template_name)

    def __add_action(self, schemaname, tablename, tsn, template_code = None):
        """adds a new action in collorg.application.action"""
        self.__set_template_module_string(schemaname, tablename, tsn)
        fqtn = "{}.{}".format(schemaname, tablename)
        module = self.db_.table(
            'collorg.core.data_type', fqtn_ = fqtn)
        if module.is_empty():
            module.insert()
        action = self.db_.table('collorg.application.action', name_ = tsn)
        action._data_type_ = module
        if action.is_empty():
            print("+ new action {}.{} {}".format(schemaname, tablename, tsn))
            action.source_.value = template_code
            self.__treat_pragmas(action)

    def __remove_cog_templates(self):
        """
        For each action in the database, check if the source is still
        here and removes it from the database if not.
        """
        import collorg
        cog_base_dir = collorg.__path__[0]
        cog_app_pkg_dir = "{}/{}".format(self.__repos_base_dir, self.pkg_path)
        action = self.db_.table('collorg.application.action')
        action.this_application_.value = True
        for act in action:
            missing = False
            data_type = act.data_type_.value
            data_type_path = self.__get_pkg_path(
                data_type.replace('.', '/'))
            src_path = "{}/{}/templates/__src/{}".format(
                cog_app_pkg_dir, data_type_path, act.name_)
            src_path_cog = "{}/{}/templates/{}.cog".format(
                cog_app_pkg_dir, data_type_path, act.name_)
            if((data_type.find("collorg.") == 0 and
                self.db_.name == "collorg_db") or
               (data_type.find("collorg.") == -1 and
                self.db_.name != "collorg_db")):
                if (not os.path.exists(src_path) and
                    not os.path.exists(src_path_cog)):
                    print("MISSING: {}".format(src_path))
                    missing = True
            elif((data_type.find("collorg.") == 0 and
                self.db_.name != "collorg_db")):
                act_cog = self.__collorg_db.table('collorg.application.action')
                act_cog.name_.value = act.name_.value
                act_cog.data_type_.value = data_type
                if act_cog.is_empty():
                    print("MISSING: {}, {}".format(data_type, act.name_))
                    missing = True
            if missing:
                module_path = [
                    "{}/{}/templates/{}".format(
                        cog_app_pkg_dir, data_type_path, act.name_),
                    "{}/db/{}/templates/{}*".format(
                    cog_base_dir, data_type_path, act.name_),
                    "{}/build/*/db/{}/templates/{}".format(
                        self.__repos_base_dir, data_type_path, act.name_)]
                for mp_ in module_path:
                    for ext in ["py", "pyc", "pyo"]:
                        file_ = "{}.{}".format(mp_, ext)
                        if os.path.exists(file_):
                            os.popen("sudo rm -f {}".format(file_))
                            print("-{}".format(file_))
                act._rev_check_requires_.delete()
                act._rev_check_required_.delete()
                act._rev_a_action_task_.delete()
                act.delete()
                print("- action removed")

    def __get_templates(self, path):
        l_templates = []
        try:
            l_files = os.listdir(path)
        except:
            # first time. the path doesn't exist
            return l_templates
        for file_ in l_files:
            if (file_.find('.cog') != -1 or
                path.find('__src') != -1 and file_.find('.') == -1):
                l_templates.append(
                    (file_.replace('.cog', ''), path.replace('/__src', '')))
                if path.find('__src') != -1:
                    new_path = path.replace('__src', '')
                    template_name = "{}/{}.cog".format(
                        new_path, file_)
                    open(template_name, "w").write(open(
                        "{}/{}".format(path, file_)).read())
        # if l_templates is empty we might be with an old __src...
        if not l_templates and path.find('__src') == -1:
            return self.__get_templates("{}/__src".format(path))
        return l_templates

    def __gen_templates(self):
        """
        Check les rép. <db>/<schema>/<module>/templates/__src/<fichier>
        Parse chaque fichier et génère un module "<fichier>.py" dans le rép.
        <db>/<schema>/templates/<module>/.
        Insert dans la table action la réf. à la template
        """
        self.this_application = True
        self.__remove_cog_templates()
        cog_app_pkg_dir = "{}/{}".format(self.__repos_base_dir, self.pkg_path)
        for schema in self.db_.schemas:
            os.chdir(cog_app_pkg_dir)
            schema_path = schema.name.replace(".", "/")
            if self.db_.name == 'collorg_db':
                schema_path = schema_path.replace("collorg/", "")
            if not os.path.exists(schema_path):
                continue
            os.chdir(schema_path)
            for tablename in schema.tables:
                # parcours du rép. <tablename>/templates/
                path = "{}/{}".format(tablename, glob.templates_dir)
                init_content = []
                init_file = "{}/__init__.py".format(path)
                # tsp: template source path
                # tsn: template source name
                for tsn, tsp in self.__get_templates(path):
                    parser = Parser()
                    # tsn must be compatible with a python method name
                    if not((tsn[0].isalpha() or tsn[0] == '_') and
                            (tsn[1:].replace('_', '').isalnum())):
                        continue
                    src_file = "{}/{}.cog".format(tsp, tsn)
                    template_src = open(src_file).read()
                    template_code = parser.parse(
                        tsn, template_src, "{}.cog".format(tsn))
                    template_sha = hashlib.sha1(template_code).hexdigest()
                    template_module_name = "{}/{}.py".format(tsp, tsn)
                    self.this_application = True
                    if (self.db_.name != 'collorg_db' and
                    schema.name.find('collorg.') == 0):
                        self.this_application = False
                    module_sha = None
                    if os.path.exists(template_module_name):
                        module_sha = hashlib.sha1(
                            open(template_module_name).read()).hexdigest()
                    if template_sha != module_sha:
                        print("+ template modified: {}".format(src_file))
                        if os.path.exists(template_module_name):
                            os.unlink(template_module_name)
                        open(template_module_name, "w").write(template_code)
                        os.chmod(template_module_name, 0444)
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
        os.chdir(self.__repos_base_dir)
