#!/usr/bin/env python
#-*- coding:  utf-8 -*-

from collorg.controller.controller import Controller

from unittest import TestCase
from .. import cog_db, cog_table

class Test(TestCase):
    def reset(self):
        self.set = cog_table('collorg.core.base_table')
        self.set_1 = self.set()
        self.subset_1_2 = self.set()
        self.set_2 = self.set()
        self.set_3 = self.set()
        self.comp_set_1 = self.set()
        self.empty_set = self.set()

    def setUp(self):
        self.reset()
        #XXX WARNING! The full set must be defined by a constraint...
        self.set.cog_oid_.set_intention('%', 'like')
        #XXX ... Otherwise, the SQL is buggy.
        self.set_1.cog_oid_.set_intention('a%', 'like')
        self.set_2.cog_oid_.set_intention('_a%', 'like')
        self.subset_1_2.cog_oid_.set_intention('aa%', 'like')
        self.set_3.cog_oid_.set_intention('__a%', 'like')
        self.comp_set_1.cog_oid_.set_intention('a%', 'not like')
        self.empty_set.cog_oid_.set_intention('X')

    def and_test(self):
        for elt in self.set_1 * self.set_2:
            self.assertTrue(
                elt.cog_oid_.value[0] == 'a' and
                elt.cog_oid_.value[1] == 'a')
        self.assertTrue(self.set_1 * self.set_1 == self.set_1)
        self.assertTrue(self.set_1 * self.subset_1_2 == self.subset_1_2)
        self.assertTrue(self.set_2 * self.subset_1_2 == self.subset_1_2)
        self.assertTrue(self.set_1 * self.set_2 == self.subset_1_2)

    def and_absorbing_elt_test(self):
        self.assertTrue(self.set_1 * self.empty_set == self.empty_set)

    def and_neutral_elt_test(self):
        self.assertTrue(self.set * self.set_1 == self.set_1)

    def or_test(self):
        for elt in self.set_1 * self.set_2 * self.set_3:
            self.assertTrue(
                elt.cog_oid_.value[0] == 'a' or
                elt.cog_oid_.value[1] == 'a' or
                elt.cog_oid_.value[2] == 'a')
        self.assertTrue(self.set_1 + self.subset_1_2 == self.set_1)
        self.assertTrue(self.set_2 + self.subset_1_2 == self.set_2)

    def or_neutral_elt_test(self):
        self.assertTrue(self.set_1 + self.empty_set == self.set_1)
    def or_absorbing_elt_test(self):
        self.assertTrue(self.set + self.set_1 == self.set)
        self.assertTrue(self.set_1 + self.set == self.set)

    def not_test(self):
        for elt in self.set_1 - self.set_2:
            self.assertTrue(
                elt.cog_oid_.value[0] == 'a' and
                elt.cog_oid_.value[1] != 'a')
        self.assertTrue(self.set_1 - self.empty_set == self.set_1)

    def empty_test(self):
        self.assertEqual((self.set_1 - self.set_1).count(), 0)
        self.assertEqual((self.set_2 - self.set_2).count(), 0)
        self.assertEqual((self.set_3 - self.set_3).count(), 0)

    def complementary_test(self):
        self.assertEqual(
            (self.set_1 + self.comp_set_1).count(), self.set.count())
        self.assertEqual(
            (self.set_1 - self.comp_set_1).count(), self.set_1.count())

    def symetric_difference_test(self):
        self.assertTrue(
            (self.set_1 - self.set_2) + (self.set_2 - self.set_1) ==
            (self.set_1 + self.set_2) - (self.set_1 * self.set_2))
        # commutativity
        self.assertTrue(
            (self.set_1 - self.set_2) + (self.set_2 - self.set_1) ==
            (self.set_2 - self.set_1) + (self.set_1 - self.set_2))

