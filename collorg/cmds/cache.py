#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import argparse
from collorg.controller.controller import Controller
from collorg.utils.cache.server import Server
from collorg.utils.cache.client import Client

class Cmd():
    def __init__(self, nop, *args):
        self.__ctrl = None
        self.__parse_args()

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog cache")
        parser.add_argument(
            "sub_cmd",
            help = "sub command: start, stop, restart, dump, clean")
        parser.add_argument(
            "-d", "--db_name",
            help = "database name")
        self.__args = parser.parse_args()
        db_name = self.__args.db_name
        if db_name:
            self.__ctrl = Controller(db_name)
            self.db = self.__ctrl.db
        else:
            self.__ctrl = Controller()
        sub_cmd = self.__args.sub_cmd
        if not sub_cmd in [
            'start', 'stop', 'restart', 'dump', 'clean',
            'bg_start', 'bg_stop']:
            parser.print_help()
            sys.exit(1)
        self.__class__.__dict__["do_{}".format(sub_cmd)](self)

    def do_bg_start(self):
        Server(self.__ctrl).start()

    def do_bg_stop(self):
        Server(self.__ctrl).stop()

    def do_start(self):
        os.system("nohup cog cache -d {} bg_start &".format(
            self.__ctrl.db.name))

    def do_stop(self):
        os.system("nohup cog cache -d {} bg_stop &".format(
            self.__ctrl.db.name))

    def do_restart(self):
        self.do_stop()
        self.do_start()

    def do_dump(self):
        Client(self.__ctrl).dump()

    def do_clean(self):
        raise NotImplementedError
