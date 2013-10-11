#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
this script <requires> <required>
requires : <fqtn>.<method_name>
required : <fqtn>.<method_name>

required is a template that is considered True if anything is printed,
False otherwise.
"""

class Action_requirement(object):
    def __init__(self, controller):
        self.__ctrl = controller
        self.__table = controller.db.table
        self._d_csv_requirement = {}
        self._d_db_requirement = {}

    def __read_csv_file(self):
        dcsv = {}
        try:
            file_ = "{}/data_files/actions/requirement.csv".format(
                self.__ctrl.repos_path)
            lines = open(file_).readlines()
        except:
            print("No {} requirement file".format(file_))
            lines = []
        if self.__ctrl.db.name != 'collorg_db':
            lines += open("{}/actions/requirement.csv".format(
                self.__ctrl.db._cog_params['application_basedir'])
                ).readlines()
        for line in lines:
            requires, required = line.strip().split(':')
            dcsv[(requires,required)] = True
        return dcsv

    def __read_db_requirement(self):
        """
        Reads from collorg.application.check (actions requirement) and
        strores the result in self._d_db_requirement dictionary
        """
        ddb = {}
        var = self.__table('collorg.application.view.action_requirement')
        var.cog_light = True
        for elt in var:
            requires = '{}.{}'.format(
                elt.requires_data_type_, elt.requires_name_)
            required = '{}.{}'.format(
                elt.required_data_type_, elt.required_name_)
            ddb[(requires,required)] = (elt.requires_oid_, elt.required_oid_)
        return ddb

    def update_check(self):
        self._d_csv_requirement = self.__read_csv_file()
        self._d_db_requirement = self.__read_db_requirement()
        for key, val in self._d_db_requirement.items():
            if not key in self._d_csv_requirement.keys():
                check = self.__table('collorg.application.check')
                check.requires_.set_intention(val[0])
                check.required_.set_intention(val[1])
                print("- removing action requirement {}".format(key))
                check.delete()
        for key in self._d_csv_requirement.keys():
            fqtn_requires, method_requires = key[0].rsplit(".", 1)
            fqtn_required, method_required = key[1].rsplit(".", 1)
            mrs = self.__table(
                'collorg.application.action',
                name_ = method_requires, data_type_ = fqtn_requires)
            mrs.get()
            mrd = self.__table(
                'collorg.application.action',
                name_ = method_required, data_type_ = fqtn_required)
            mrd.get()
            check = self.__table('collorg.application.check')
            check._requires_ = mrs
            check._required_ = mrd
            if not check.exists():
                print("+ adding action requirement {}".format(key))
                check.insert()
