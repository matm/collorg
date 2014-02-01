#!/usr/bin/env python
#-*- coding:  utf-8 -*-

from collorg.controller.controller import Controller

from random import randint
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
        hexchars = '0123456789abcdef'
        self.reset()
        self.c1 = hexchars[randint(0,15)]
        self.c2 = hexchars[randint(0,15)]
        self.c3 = hexchars[randint(0,15)]
        #XXX WARNING! The full set must be defined by a constraint...
        self.set.cog_oid_.set_intention('%', 'like')
        #XXX ... Otherwise, the SQL is buggy.
        self.set_1.cog_oid_.set_intention('{}%'.format(self.c1), 'like')
        self.set_2.cog_oid_.set_intention('_{}%'.format(self.c2), 'like')
        self.subset_1_2.cog_oid_.set_intention(
            '{}{}%'.format(self.c1, self.c2), 'like')
        self.set_3.cog_oid_.set_intention('__{}%'.format(self.c3), 'like')
        self.comp_set_1.cog_oid_.set_intention('{}%'.format(self.c1), 'not like')
        self.empty_set.cog_oid_.set_intention('X')

    def and_test(self):
        for elt in self.set_1 * self.set_2:
            self.assertTrue(
                elt.cog_oid_.value[0] == self.c1 and
                elt.cog_oid_.value[1] == self.c2)
        self.assertTrue(self.set_1 * self.set_1 == self.set_1)
        self.assertTrue(self.set_1 * self.subset_1_2 == self.subset_1_2)
        self.assertTrue(self.set_2 * self.subset_1_2 == self.subset_1_2)
        self.assertTrue(self.set_1 * self.set_2 == self.subset_1_2)

    def and_absorbing_elt_test(self):
        self.assertTrue(self.set_1 * self.empty_set == self.empty_set)

    def and_neutral_elt_test(self):
        self.assertTrue(self.set * self.set_1 == self.set_1)

    def or_test(self):
        for elt in self.set_1 + (self.set_2 + self.set_3):
            self.assertTrue(
                elt.cog_oid_.value[0] == self.c1 or
                elt.cog_oid_.value[1] == self.c2 or
                elt.cog_oid_.value[2] == self.c3)
        self.assertTrue(self.set_1 + self.subset_1_2 == self.set_1)
        self.assertTrue(self.set_2 + self.subset_1_2 == self.set_2)

    def or_neutral_elt_test(self):
        self.assertTrue(self.set_1 + self.empty_set == self.set_1)
    def or_absorbing_elt_test(self):
        self.assertTrue(self.set + self.set_1 == self.set)
        self.assertTrue(self.set_1 + self.set == self.set)
        self.assertTrue(self.empty_set + self.empty_set == self.empty_set)

    def not_test(self):
        for elt in self.set_1 - self.set_2:
            self.assertTrue(
                elt.cog_oid_.value[0] == self.c1 and
                elt.cog_oid_.value[1] != self.c2)
        self.assertTrue(self.set_1 - self.empty_set == self.set_1)

    def empty_test(self):
        self.assertTrue(self.set_1 - self.set_1 == self.empty_set)
        self.assertTrue(self.set_2 - self.set_2 == self.empty_set)
        self.assertTrue(self.set_3 - self.set_3 == self.empty_set)
        self.assertTrue(self.set - self.set == self.empty_set)

    def complementary_test(self):
        self.assertTrue(self.set_1 + self.comp_set_1 == self.set)
        self.assertTrue(self.set_1 - self.comp_set_1 == self.set_1)

    def symetric_difference_test(self):
        self.assertTrue(
            (self.set_1 - self.set_2) + (self.set_2 - self.set_1) ==
            (self.set_1 + self.set_2) - (self.set_1 * self.set_2))
        # commutativity
        self.assertTrue(
            (self.set_1 - self.set_2) + (self.set_2 - self.set_1) ==
            (self.set_2 - self.set_1) + (self.set_1 - self.set_2))

    def commutative_laws_test(self):
        self.assertTrue(self.set_1 + self.set_2 == self.set_2 + self.set_1)
        self.assertTrue(self.set_1 * self.set_2 == self.set_2 * self.set_1)

    def associative_laws_test(self):
        self.assertTrue(self.set_1 + (self.set_2 + self.set_3) ==
                        (self.set_1 + self.set_2) + self.set_3)
        self.assertTrue(self.set_1 * (self.set_2 * self.set_3) ==
                        (self.set_1 * self.set_2) * self.set_3)

    def distributive_laws_test(self):
        self.assertTrue(self.set_1 + (self.set_2 * self.set_3) ==
                        (self.set_1 + self.set_2) * (self.set_1 + self.set_3))
        self.assertTrue(self.set_1 * (self.set_2 + self.set_3) ==
                        (self.set_1 * self.set_2) + (self.set_1 * self.set_3))

    def identity_laws_test(self):
        self.assertTrue(self.set_1 + self.empty_set == self.set_1)
        self.assertTrue(self.set_1 * self.set == self.set_1)

    def complement_laws_test(self):
        self.assertTrue(self.set_1 + self.comp_set_1 == self.set)
        self.assertTrue(self.set_1 * self.comp_set_1 == self.empty_set)
        self.assertTrue(self.set_1 + (-self.set_1) == self.set)
        self.assertTrue(self.set_1 * (-self.set_1) == self.empty_set)

    def idempotent_laws_test(self):
        self.assertTrue(self.set_1 + self.set_1 == self.set_1)
        self.assertTrue(self.set_1 * self.set_1 == self.set_1)

    def domination_laws_test(self):
        self.assertTrue(self.set_1 + self.set == self.set)
        self.assertTrue(self.set_1 * self.empty_set == self.empty_set)

    def absorption_laws_test(self):
        self.assertTrue(self.set_1 + (self.set_1 * self.set_2) == self.set_1)
        self.assertTrue(self.set_1 * (self.set_1 + self.set_2) == self.set_1)

    def de_morgan_s_laws_test(self):
        print("--   -(self.set_1 * self.set_2)")
        print((-(self.set_1 * self.set_2)).select(just_return_sql=True))
        print("--   (-self.set_1) + (-self.set_2)")
        print(((-self.set_1) + (-self.set_2)).select(just_return_sql=True))
        a = (-self.set_1) + (-self.set_2)
        b = -(self.set_1 * self.set_2)
        self.assertTrue(a == b)
        self.assertTrue(
            -(self.set_1 + self.set_2) == (-self.set_1) * (-self.set_2))

    def double_complement_law(self):
        self.assertTrue(-(-self.set_1) == self.set_1)
