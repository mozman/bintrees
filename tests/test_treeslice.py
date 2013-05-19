#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Created: 11.04.2011
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License


import unittest

from bintrees import RBTree


class TestTreeSlice(unittest.TestCase):
    def setUp(self):
        self.tree = RBTree({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'})

    def test_in_slice_object(self):
        treeslice = self.tree[2:6]
        self.assertTrue(2 in treeslice)

    def test_not_in_slice_object(self):
        treeslice = self.tree[2:6]
        self.assertFalse(1 in treeslice)

    def test_in_slice_object_with_no_start(self):
        treeslice = self.tree[:6]
        self.assertTrue(1 in treeslice)
        self.assertFalse(6 in treeslice)

    def test_in_slice_object_with_no_stop(self):
        treeslice = self.tree[2:]
        self.assertTrue(6 in treeslice)
        self.assertFalse(1 in treeslice)

    def test_getitem_from_slice_object(self):
        treeslice = self.tree[2:6]
        self.assertEqual('b', treeslice[2])

    def test_error_getitem_for_key_out_of_range(self):
        treeslice = self.tree[2:6]
        self.assertRaises(KeyError, treeslice.__getitem__, 6)
        self.assertRaises(KeyError, treeslice.__getitem__, 1)

    def test_error_getitem_for_key_in_range(self):
        treeslice = self.tree[2:6]
        self.assertRaises(KeyError, treeslice.__getitem__, 3.5)

    def test_iter_slice_object(self):
        treeslice = self.tree[2:6]
        self.assertEqual([2, 3, 4, 5], list(treeslice))

    def test_iter_all(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], list(self.tree[:]))

    def test_iter_values_slice_object(self):
        treeslice = self.tree[2:6]
        self.assertEqual(['b', 'c', 'd', 'e'], list(treeslice.values()))

    def test_iter_items_slice_object(self):
        treeslice = self.tree[2:6]
        self.assertEqual([(2, 'b'), (3, 'c'), (4, 'd'), (5, 'e')], list(treeslice.items()))

    def test_subslicing(self):
        subslice = self.tree[2:6][3:5]
        self.assertEqual([3, 4], list(subslice))

    def test_subslicing_nobounds_1(self):
        subslice = self.tree[2:6][:5]
        self.assertEqual([2, 3, 4], list(subslice))

    def test_subslicing_nobounds_2(self):
        subslice = self.tree[2:6][3:]
        self.assertEqual([3, 4, 5], list(subslice))

    def test_subslicing_nobounds_3(self):
        subslice = self.tree[:4][:3]
        self.assertEqual([1, 2], list(subslice))

    def test_subslicing_nobounds_4(self):
        subslice = self.tree[:4][2:]
        self.assertEqual([2, 3], list(subslice))

    def test_subslicing_nobounds_5(self):
        subslice = self.tree[2:][1:]
        self.assertEqual([2, 3, 4, 5, 6], list(subslice))

    def test_subslicing_nobounds_6(self):
        subslice = self.tree[2:][:5]
        self.assertEqual([2, 3, 4], list(subslice))

    def test_subslicing_nobounds_7(self):
        subslice = self.tree[2:][:1]
        self.assertEqual([], list(subslice))

    def test_repr(self):
        result = repr(self.tree[2:4])
        self.assertEqual("RBTree({2: 'b', 3: 'c'})", result)

if __name__ == '__main__':
    unittest.main()