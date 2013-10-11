#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
from collorg.controller.controller import Controller

class Cmd():
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.db = self.__ctrl.db
        self.__repos_base_dir = self.__ctrl.repos_path
        self.__parse_args()

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog template")
        parser.add_argument(
            "-a", "--an_arg", help = "an argument", required = True)
        self.__args = parser.parse_args()
