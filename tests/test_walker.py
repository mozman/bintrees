#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Created: 08.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

import unittest
from bintrees import BinaryTree, FastBinaryTree

testkeys = [10, 5, 15, 3, 7, 12, 20, 1, 4, 6, 8, 30]
testitems = list(zip(testkeys, testkeys))


class WalkerCheck:
    def get_tree(self, items):
        return BinaryTree(items)

    def test_goto_key_exists(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        # returns True if key found
        self.assertTrue(walker.goto(30))
        self.assertEqual(walker.key, 30)

    def test_goto_key_above(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        # returns True if key found
        self.assertTrue(walker.goto(30))
        self.assertEqual(walker.key, 30)
        self.assertTrue(walker.goto(12))
        self.assertTrue(walker.goto(4))

    def test_key_value_item_properties(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(6)
        self.assertEqual(walker.key, 6)
        self.assertEqual(walker.value, 6)
        self.assertEqual(walker.item, (6, 6))

    def test_goto_key_not_exists(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        self.assertFalse(walker.goto(41))

    def test_reset(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        self.assertTrue(walker.goto(12))
        self.assertEqual(walker.key, 12)
        self.assertEqual(walker.value, 12)
        walker.reset()
        self.assertEqual(walker.key, 10)
        self.assertEqual(walker.value, 10)

    def test_is_valid(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(30)
        self.assertTrue(walker.is_valid)

    def test_is_not_valid(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(41)
        self.assertFalse(walker.is_valid)

    def test_push_pop(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(15)
        walker.push()
        walker.go_left()
        self.assertEqual(walker.key, 12)
        walker.pop()
        self.assertEqual(walker.key, 15)

    def test_stack(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(15)
        walker.push()
        self.assertFalse(walker.stack_is_empty())
        walker.pop()
        self.assertTrue(walker.stack_is_empty())

    def test_stack_error(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        self.assertTrue(walker.stack_is_empty())
        self.assertRaises(IndexError, walker.pop)

    def test_goto_leaf(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto_leaf()
        self.assertTrue(walker.key in [1, 4, 6, 8, 12, 30])

    def test_down(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.push()
        walker.down(0)  # left
        self.assertEqual(walker.key, 5)
        walker.pop()
        walker.down(1)  # right
        self.assertEqual(walker.key, 15)

    def test_has_left_right(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(7)
        self.assertTrue(walker.has_left())
        self.assertTrue(walker.has_right())
        walker.goto(12)
        self.assertFalse(walker.has_left())
        self.assertFalse(walker.has_right())

    def test_has_child(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        walker.goto(7)
        self.assertTrue(walker.has_child(0))
        self.assertTrue(walker.has_child(1))
        walker.goto(20)
        self.assertFalse(walker.has_child(0))
        self.assertTrue(walker.has_child(1))

    def test_prev(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        item = walker.prev_item(8)
        self.assertEqual(item[0], 7)
        item = walker.prev_item(6)
        self.assertEqual(item[0], 5)
        item = walker.prev_item(12)
        self.assertEqual(item[0], 10)
        item = walker.prev_item(10)
        self.assertEqual(item[0], 8)

    def test_succ(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        item = walker.succ_item(7)
        self.assertEqual(item[0], 8)
        item = walker.succ_item(10)
        self.assertEqual(item[0], 12)
        item = walker.succ_item(20)
        self.assertEqual(item[0], 30)

    def test_floor_item(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        with self.assertRaises(KeyError):
            walker.floor_item(0)
        self.assertEqual(walker.floor_item(2)[0], 1)
        self.assertEqual(walker.floor_item(3)[0], 3)
        self.assertEqual(walker.floor_item(8)[0], 8)
        self.assertEqual(walker.floor_item(9)[0], 8)
        self.assertEqual(walker.floor_item(11)[0], 10)
        self.assertEqual(walker.floor_item(13)[0], 12)
        self.assertEqual(walker.floor_item(14)[0], 12)
        self.assertEqual(walker.floor_item(16)[0], 15)
        self.assertEqual(walker.floor_item(21)[0], 20)
        self.assertEqual(walker.floor_item(31)[0], 30)

    def test_ceiling_item(self):
        tree = self.get_tree(testitems)
        walker = tree.get_walker()
        with self.assertRaises(KeyError):
            walker.ceiling_item(50)
        self.assertEqual(walker.ceiling_item(30)[0], 30)
        self.assertEqual(walker.ceiling_item(29)[0], 30)
        self.assertEqual(walker.ceiling_item(19)[0], 20)
        self.assertEqual(walker.ceiling_item(13)[0], 15)
        self.assertEqual(walker.ceiling_item(11)[0], 12)
        self.assertEqual(walker.ceiling_item(10)[0], 10)
        self.assertEqual(walker.ceiling_item(9)[0], 10)
        self.assertEqual(walker.ceiling_item(8)[0], 8)
        self.assertEqual(walker.ceiling_item(2)[0], 3)
        self.assertEqual(walker.ceiling_item(1)[0], 1)
        self.assertEqual(walker.ceiling_item(0)[0], 1)


class TestPythonWalker(WalkerCheck, unittest.TestCase):
    def get_tree(self, items):
        return BinaryTree(items)


class TestWalker(WalkerCheck, unittest.TestCase):
    def get_tree(self, items):
        return FastBinaryTree(items)

if __name__ == '__main__':
    unittest.main()