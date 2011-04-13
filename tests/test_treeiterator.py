#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test TreeIterator
# Created: 04.05.2010

import sys
import unittest

from bintrees import BinaryTree
from bintrees import TreeIterator

keys = [5, 8, 2, 9, 7, 1]

class TestTreeIterator(unittest.TestCase):
    def test_init(self):
        tree = BinaryTree.fromkeys(keys)
        treeiter = TreeIterator(tree)
        self.assertEqual(treeiter.next(), 1)

    def test_iterkeys_ascending(self):
        tree = BinaryTree.fromkeys(keys)
        treeiter = TreeIterator(tree)
        for key, chk in zip(treeiter, sorted(keys)):
            self.assertEqual(key, chk)

    def test_iterkeys_descending(self):
        tree = BinaryTree.fromkeys(keys)
        treeiter = TreeIterator(tree, reverse=True)
        for key, chk in zip(treeiter, sorted(keys, reverse=True)):
            self.assertEqual(key, chk)

    def test_iterkeys_next_prev(self):
        tree = BinaryTree.fromkeys(keys)
        treeiter = TreeIterator(tree)
        self.assertEqual(treeiter.next(), 1)
        self.assertEqual(treeiter.next(), 2)
        self.assertEqual(treeiter.prev(), 1)
        self.assertRaises(StopIteration, treeiter.prev)

    def test_iterkeys_goto(self):
        tree = BinaryTree.fromkeys(keys)
        treeiter = TreeIterator(tree)
        treeiter.goto(8)
        self.assertEqual(treeiter.prev(), 7)
        self.assertEqual(treeiter.next(), 8)
        self.assertEqual(treeiter.next(), 9)
        self.assertRaises(StopIteration, treeiter.next)

    def test_iterkeys_goto_error(self):
        tree = BinaryTree.fromkeys(keys)
        treeiter = TreeIterator(tree)
        self.assertRaises(KeyError, treeiter.goto, 17)

    def test_iterkeys_rtype_value(self):
        tree = BinaryTree([(1, 'one'), (2, 'two'), (3, 'three')])
        treeiter = TreeIterator(tree, rtype='value')
        self.assertEqual(treeiter.next(), 'one')
        self.assertEqual(treeiter.next(), 'two')

    def test_iterkeys_rtype_item(self):
        tree = BinaryTree([(1, 'one'), (2, 'two'), (3, 'three')])
        treeiter = TreeIterator(tree, rtype='item')
        item = next(treeiter)
        self.assertEqual(item[0], 1)
        self.assertEqual(item[1], 'one')

if __name__=='__main__':
    unittest.main()