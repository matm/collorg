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
        a = self.set_1
        b = self.set_2
        ab = self.subset_1_2
        self.assertTrue(a * b == a - ( a - b))
        self.assertTrue(a * b == ((a + b) - (a - b) - ( b - a)))
        self.assertTrue(a * a == a)
        self.assertTrue(a * ab == ab)
        self.assertTrue(b * ab == ab)
        self.assertTrue(a * b == ab)

    def and_absorbing_elt_test(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(a * empty == empty)

    def and_neutral_elt_test(self):
        a = self.set_1
        universe = self.set
        self.assertTrue(universe * a == a)

    def or_test(self):
        a = self.set_1
        b = self.set_2
        ab = self.subset_1_2
        self.assertTrue(a + ab == a)
        self.assertTrue(b + ab == b)

    def or_neutral_elt_test(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(a + empty == a)

    def or_absorbing_elt_test_1(self):
        a = self.set_1
        universe = self.set
        self.assertTrue(universe + a == universe)

    def or_absorbing_elt_test_2(self):
        a = self.set_1
        universe = self.set
        self.assertTrue(a + universe == universe)

    def or_absorbing_elt_test_3(self):
        empty = self.empty_set
        self.assertTrue(empty + empty == empty)

    def not_test(self):
        a = self.set_1
        b = self.set_2
        empty = self.empty_set
#        for elt in a - b:
#            self.assertTrue(
#                elt.cog_oid_.value[0] == self.c1 and
#                elt.cog_oid_.value[1] != self.c2)
        self.assertTrue(a - empty == a)

    def empty_test(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        empty = self.empty_set
        universe = self.set
        self.assertTrue(a - a == empty)
        self.assertTrue(b - b == empty)
        self.assertTrue(c - c == empty)
        self.assertTrue(universe - universe == empty)

    def complementary_test_1(self):
        a = self.set_1
        comp_a = self.comp_set_1
        universe = self.set
        self.assertTrue(a + comp_a == universe)

    def complementary_test_2(self):
        a = self.set_1
        comp_a = self.comp_set_1
        self.assertTrue(a - comp_a == a)

    def symetric_difference_test(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(
            (self.set_1 - self.set_2) + (self.set_2 - self.set_1) ==
            (self.set_1 + self.set_2) - (self.set_1 * self.set_2))

    def commutative_laws_test(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(a + b == b + a)
        self.assertTrue(a * b == b * a)

    def associative_laws_test(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue(a + (b + c) == (a + b) + c)
        self.assertTrue(a * (b * c) == (a * b) * c)

    def distributive_laws_test(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue(a + (b * c) == (a + b) * (a + c))
        self.assertTrue(a * (b + c) == (a * b) + (a * c))

    def identity_laws_test(self):
        a = self.set_1
        empty = self.empty_set
        universe = self.set
        self.assertTrue(a + empty == a)
        self.assertTrue(a * universe == a)

    def complement_laws_test_1(self):
        a = self.set_1
        comp_a = self.comp_set_1
        universe = self.set
        self.assertTrue(a + comp_a == universe)

    def complement_laws_test_2(self):
        a = self.set_1
        comp_a = self.comp_set_1
        empty = self.empty_set
        self.assertTrue(a * comp_a == empty)

    def complement_laws_test_3(self):
        a = self.set_1
        universe = self.set
        self.assertTrue(a + (-a) == universe)

    def complement_laws_test_4(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(a * (-a) == empty)

    def idempotent_laws_test_1(self):
        a = self.set_1
        self.assertTrue(a + a == a)

    def idempotent_laws_test_2(self):
        a = self.set_1
        self.assertTrue(a * a == a)

    def domination_laws_test_1(self):
        a = self.set_1
        universe = self.set
        self.assertTrue(a + universe == universe)

    def domination_laws_test_2(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(a * empty == empty)

    def absorption_laws_test(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(a + (a * b) == a)
        self.assertTrue(a * (a + b) == a)

    def de_morgan_s_laws_test_1(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue((-a) + (-b) == -(a * b))

    def de_morgan_s_laws_test_2(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(-(a + b) == (-a) * (-b))

    def double_complement_law_test(self):
        a = self.set_1
        self.assertTrue(-(-a) == a)

    def empty_universe_complement_test_1(self):
        universe = self.set
        empty = self.empty_set
        self.assertTrue(-empty == universe)

    def empty_universe_complement_test_2(self):
        universe = self.set
        empty = self.empty_set
        self.assertTrue(-universe == empty)

    def inclusion_test_1(self):
        a = self.set_1
        b = self.set_2
        ab = self.subset_1_2
        self.assertTrue(ab in a)
        self.assertTrue(ab in b)
        self.assertTrue(ab in a * b)

    def inclusion_test_2(self):
        a = self.set_1
        b = self.set_2
        empty = self.empty_set
        self.assertTrue(empty in a)

    def inclusion_test_3(self):
        a = self.set_1
        b = self.set_2
        universe = self.set
        self.assertTrue(a in universe)

    def inclusion_test_4(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(a in a + b)
        self.assertTrue(b in a + b)

    def inclusion_test_5(self):
        a = self.set_1
        ab = self.subset_1_2
        empty = self.empty_set
        self.assertTrue(ab - a == empty)

    def inclusion_test_6(self):
        a = self.set_1
        ab = self.subset_1_2
        self.assertTrue(-a in -ab)

    def relative_complement_test_1(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue(c - (a * b) == (c - a) + (c - b))

    def relative_complement_test_2(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue(c - (a + b) == (c - a) * (c - b))

    def relative_complement_test_3(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue(c - (b - a) == (a * c) + (c - b))

    def relative_complement_test_4(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue((b - a) * c == (b * c) - a)

    def relative_complement_test_5(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue((b - a) * c == b * (c - a))

    def relative_complement_test_6(self):
        a = self.set_1
        b = self.set_2
        c = self.set_3
        self.assertTrue((b - a) + c == (b + c) - (a - c))

    def relative_complement_test_7(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(a - a == empty)

    def relative_complement_test_8(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(empty - a == empty)

    def relative_complement_test_9(self):
        a = self.set_1
        empty = self.empty_set
        self.assertTrue(a - empty == a)

    def relative_complement_test_10(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(b - a == -a * b)

    def relative_complement_test_11(self):
        a = self.set_1
        b = self.set_2
        self.assertTrue(-(b - a) == a + (-b))

    def relative_complement_test_12(self):
        a = self.set_1
        universe = self.set
        self.assertTrue(universe - a == -a)

    def relative_complement_test_13(self):
        a = self.set_1
        empty = self.empty_set
        universe = self.set
        self.assertTrue(a - universe == empty)
