#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
from collorg.controller.controller import Controller
from collorg.utils.mail import Mail

"""
Add users from file.
A line must be in the format :
<first Name>,<last Name>,<email>,<pseudo>
"""

if __name__ == '__main__':
    ctrl = Controller()

    db = ctrl.db
    url = "{}://{}".format(db._cog_params['url_scheme'], db._cog_params['url'])
    script_path = '/'.join(sys.argv[0].split('/')[:-1])
    sender_pseudo = sys.argv[3]
    sender = db.table('collorg.actor.user', pseudo_ = sender_pseudo).get()
    d_mesg = dict(eval(
        open("{}/std_msg_{}.txt".format(script_path, sys.argv[2])).read()))
    title = d_mesg['title']
    message = d_mesg['message']
    for line in open(sys.argv[1]):
        first_name, last_name, email, pseudo = line.strip().split(',')
        passwd = os.popen('makepasswd 2> /dev/null').read().strip()
        if not passwd:
            sys.stderr.write(
                "The makepasswd command is missing. Please install it!\n")
            sys.exit(1)
        user = db.table('collorg.actor.user')
        kwargs = {}
        kwargs['first_name_'] = first_name
        kwargs['last_name_'] = last_name
        kwargs['email_'] = email
        kwargs['pseudo_'] = pseudo
        kwargs['password_'] = passwd
        try:
            user.new_account(**kwargs)
            mail = Mail(db)
            mail.set_from(sender.email_.value)
            mail.set_to([email])
            mail.set_subject(title.format(url))
            mail.set_body(message.format(
                url, pseudo, passwd, sender.first_name_, sender.last_name_))
            mail.send()
        except Exception as err:
            print(err)
