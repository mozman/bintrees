#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License


import sys
PYPY = hasattr(sys, 'pypy_version_info')

import unittest
from random import randint, shuffle

if not PYPY:
    from bintrees.qrbtree import cRBTree

    class Tree(cRBTree):
        def update(self, items):
            """ T.update(E) -> None. Update T from E : for (k, v) in E: T[k] = v """
            try:
                generator = items.iteritems()
            except AttributeError:
                generator = iter(items)
            for key, value in generator:
                self.insert(key, value)


@unittest.skipIf(PYPY, "Cython implementation not supported for pypy.")
class TestTree(unittest.TestCase):
    values = [(2, 12), (4, 34), (8, 45), (1, 16), (9, 35), (3, 57)]
    keys = [2, 4, 8, 1, 9, 3]

    def test_create_tree(self):
        tree = Tree()
        self.assertEqual(tree.count, 0)
        tree.update(self.values)
        self.assertEqual(tree.count, 6)

    def test_properties(self):
        tree = Tree(self.values)
        self.assertEqual(tree.count, 6)

    def test_clear_tree(self):
        tree = Tree(self.values)
        tree.clear()
        self.assertEqual(tree.count, 0)

    def test_insert(self):
        tree = Tree()
        for key in self.keys:
            tree.insert(key, key)
            value = tree.get_value(key)
            self.assertEqual(value, key)
        self.assertEqual(tree.count, 6)

    def test_remove(self):
        tree = Tree(self.values)
        for key in self.keys:
            tree.remove(key)
            self.assertRaises(KeyError, tree.get_value, key)
        self.assertEqual(tree.count, 0)

    def test_remove_random_numbers(self):
        keys = list(set([randint(0, 10000) for _ in range(500)]))
        shuffle(keys)
        tree = Tree(zip(keys, keys))
        self.assertEqual(tree.count, len(keys))
        for key in keys:
            tree.remove(key)
        self.assertEqual(tree.count, 0)

    def test_data_corruption(self):
        tree = Tree()
        tree.insert(14, 777)
        tree.insert(15.84, 777)
        tree.insert(16, 777)
        tree.insert(16, 777)  # reassign
        tree.insert(16.3, 777)
        tree.insert(15.8, 777)
        tree.insert(16.48, 777)
        tree.insert(14.95, 777)
        tree.insert(15.07, 777)
        tree.insert(16.41, 777)
        tree.insert(16.43, 777)
        tree.insert(16.45, 777)
        tree.insert(16.4, 777)
        tree.insert(16.42, 777)
        tree.insert(16.47, 777)
        tree.insert(16.44, 777)
        tree.insert(16.46, 777)
        tree.insert(16.48, 777)
        tree.insert(16.51, 777)
        tree.insert(16.5, 777)
        tree.insert(16.49, 777)
        tree.insert(16.5, 777)   # reassign
        tree.insert(16.49, 777)  # reassign
        tree.insert(16.49, 777)  # reassign
        tree.insert(16.47, 777)
        tree.insert(16.5, 777)  # reassign
        tree.insert(16.48, 777)  # reassign
        tree.insert(16.46, 777)  # reassign
        tree.insert(16.44, 777)  # reassign - causes data corruption in version 1.0.1
        try:
            tree.get_value(16.43)
        except KeyError:
            self.fail("Data corruption in FastRBTree!")


if __name__ == '__main__':
    unittest.main()
