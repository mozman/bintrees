#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test cAVLTree
# Created: 28.04.2010
import sys
import unittest

if sys.platform.startswith('linux2'):
    import pyximport
    pyximport.install()

from bintrees.cavltree import cAVLTree

if sys.platform.startswith('linux2'):
    import pyximport
    pyximport.install()

class HelperTree(cAVLTree):
    def update(self, items):
        """ T.update(E) -> None. Update T from E : for (k, v) in E: T[k] = v """
        try:
            generator = items.iteritems()
        except AttributeError:
            generator = iter(items)
        for key, value in generator:
            self.insert(key, value)

class TestHelperTree(unittest.TestCase):
    default_values1 = zip([12, 34, 45, 16, 35, 57], [12, 34, 45, 16, 35, 57])
    default_values2 = [(2, 12), (4, 34), (8, 45), (1, 16), (9, 35), (3, 57)]

    def test_create_tree(self):
        tree = HelperTree()
        self.assertEqual(tree.count, 0)
        tree.update(self.default_values1)
        self.assertEqual(tree.count, 6)

if __name__=='__main__':
    unittest.main()