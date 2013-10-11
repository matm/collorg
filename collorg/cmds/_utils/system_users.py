#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collorg.controller.controller import Controller

description = """
add system users
"""

class System_users():
    std_users = [
        (None,
         'Anonymous user','collorg.actor.user',
         'Anonymous navigation', False),
        (None,
         'Authenticated user','collorg.actor.user',
         'Authenticated navigation', False),
        (None,
         'Administrator user','collorg.core.database',
         'Administrator navigation', False),
        (None,
         'Collorg actor', 'collorg.actor.user',
         None, False),
        (None,
         'Group administrator', 'collorg.group.group',
         'Group administration', False),
        (None,
         'Group member', 'collorg.group.group',
         'Group membership', False),
        (None,
         'Group moderator', 'collorg.group.group',
         'Group moderation', False),
         ]

    def __init__(self, controller):
        self.__controller = controller
        self.__db = controller.db
        self.check()

    def check(self):
        for user, function, data_type, task_name, advertise in self.std_users:
            self.__add_user(
                user, function, data_type, task_name, advertise)
        self.__add_goal()

    def __add_goal(self):
        for label, function in [
            ('Authenticated navigation','Authenticated user'),
            ('Anonymous navigation', 'Anonymous user')]:
            goal = self.__db.table('collorg.application.goal')
            goal.name_.set_intention(label)
            if not goal.exists():
                goal.insert()
            task = self.__db.table('collorg.application.task')
            task.name_.set_intention(label)
            atg = self.__db.table('collorg.application.a_task_goal')
            atg._task_ = task
            atg._goal_ = goal
            if not atg.exists():
                atg.insert()

    def __add_inst_group(self, value, data_type, advertise):
        if data_type is None:
            return
        i_group = self.__db.table('collorg.actor.inst_group')
        i_group.name_.set_intention(value)
        i_group.long_name_.set_intention(value)
        i_group.data_type_.set_intention(data_type)
        if not i_group.exists():
            i_group.insert()
        return i_group

    def __add_link_to_task(self, function, task_name):
        if task_name is None:
            return
        task = self.__db.table('collorg.application.task')
        task.name_.set_intention(task_name)
        if not task.exists():
            task.insert()
        rtf = function._rev_a_task_function_
        rtf._task_ = task
        rtf._task_ = task
        if not rtf.exists():
            print("+ Function<->Task: %s<->%s" % (
                function.long_name_.val, task_name))
            rtf.insert()

    def __add_function(self, value, data_type, task_name, advertise):
        i_group = self.__add_inst_group(value, data_type, advertise)
        func = self.__db.table('collorg.actor.function')
        func.name_.set_intention(value)
        func.fname_.set_intention(value)
        func.long_name_.set_intention(value)
        func.data_type_.set_intention(data_type)
        if not func.exists():
            func.advertise_.set_intention(advertise)
            func.insert()
            afig = self.__db.table('collorg.actor.a_function_inst_group')
            afig.inst_group_.set_intention(i_group.cog_oid_)
            afig._function_ = func
            afig.insert()
        self.__add_link_to_task(func, task_name)
        return func

    def __add_role(self, user, value, data_type, task_name, advertise):
        func = self.__add_function(value, data_type, task_name, advertise)
        role = self.__db.table('collorg.actor.role')
        role.function_.set_intention(func.cog_oid_)
        role.data_.set_intention(user.cog_oid_)
        if not role.exists():
            super(role.__class__, role).insert()
        return role

    def __add_access(self, user, role):
        access = self.__db.table('collorg.access.access')
        access.role_.set_intention(role.cog_oid_)
        access.user_.set_intention(user.cog_oid_)
        if not access.exists():
            access.insert()

    def __add_user(self, pseudo, function, data_type, task_name, advertise):
        pers = self.__db.table( 'collorg.actor.user' )
        self.__add_function(function, data_type, task_name, advertise)

if __name__ == '__main__':
    System_users(Controller())

