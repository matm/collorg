#-*- coding: utf-8 -*-

import time

from unittest import TestCase
from ... import cog_db, cog_table

class Test(TestCase):
    def setUp(self):
        self.user = cog_table('collorg.actor.user')
        gaston = self.user()
        gaston.pseudo_.set_intention('gaston')
        gaston.remove_account()

    def tearDown(self):
        self.gaston.remove_account()
        cog_db.rollback()

    def __create_gaston(self):
        self.gaston = self.user.new_account(
            first_name_ = 'Gaston',
            last_name_ = 'Lagaffe',
            password_ = "m'enfin",
            email_ = 'gaston@editions-dupuis.com',
            pseudo_ = 'gaston')

    def __check_new_account_access(self, user):
        access = user._rev_access_
        self.assertEqual(access.count(), 2)
        #XXX pb here ! If we don't do the count, we can't make the get ???
        root_topic = user._rev_post_.get()
        self.assertEqual(root_topic.cog_fqtn_.value, 'collorg.web.topic')
        self.assertTrue(user.has_access(root_topic))

    def new_account_test(self):
        self.__create_gaston()
        # can't create gaston's account twice
        self.assertRaises(RuntimeError, self.__create_gaston)
        self.__check_new_account_access(self.gaston)

