#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from collorg.controller.controller import Controller
import getpass

if __name__ == '__main__':
    ctrl = Controller()
    if len(sys.argv) == 2:
        ctrl = Controller(sys.argv[1])
    db = ctrl.db
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