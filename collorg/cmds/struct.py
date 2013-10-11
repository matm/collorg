#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
from collorg.controller.controller import Controller

class Cmd():
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.__db = self.__ctrl.db
        self.__parse_args()
        if self.__args.table and not self.__args.schema:
            # fqtn
            self.show_table(self.__args.table)
        elif self.__args.schema and self.__args.table:
            self.show_table("%s.%s" % (self.__args.schema, self.__args.table))
        elif self.__args.schema:
            self.show_schema(self.__args.schema)
        else:
            self.showstruct()

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog struct")
        parser.add_argument(
            "-s", "--schema", help = "schema name (namespace)")
        parser.add_argument(
            "-t", "--table",
            help =("table name (fully qualified table "
                "name if schema name not specified)"))
        self.__args = parser.parse_args()

    def showstruct(self):
        self.__db.showstruct()

    def show_table(self, fqtn):
        table = self.__db.table(fqtn)
        print("Table: %s\n" % fqtn)
        print("\n".join(table.showstruct()))

    def show_schema(self, schema):
        self.__db.showstruct(schema)
