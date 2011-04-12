#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test iteritemsinrange
# Created: 12.04.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from bintrees import RBTree

class OptTree(RBTree):
    def iteritemsinrange(self, start, stop):
        if self.is_empty():
            return

        def go_left_with_bound():
            return node.key > start and node.has_left() and go_down
        def go_left_without_bound():
            return node.has_left() and go_down
        go_left = go_left_without_bound if start is None else go_left_with_bound

        def go_right_with_bound():
            return node.key < stop and node.has_right()
        def go_right_without_bound():
            return node.has_right()
        go_right = go_right_without_bound if stop is None else go_right_with_bound

        if (start, stop) == (None, None):
            in_range = lambda: True
        elif start is None:
            in_range = lambda: node.key < stop
        elif stop is None:
            in_range = lambda: node.key >= start
        else:
            in_range = lambda: start <= node.key < stop

        node = self.get_walker()
        go_down = True
        while True:
            if go_left():
                node.push()
                node.go_left()
            else:
                if in_range():
                    yield node.item
                if go_right():
                    node.go_right()
                    go_down = True
                else:
                    if node.stack_is_empty():
                        return # all done
                    node.pop()
                    go_down = False

    def keysinrange(self, start, stop):
        return [item[0] for item in self.iteritemsinrange(start, stop)]

class TestOptimizedRangeIterator(unittest.TestCase):
    def setUp(self):
        self.tree = OptTree({1:'a', 2:'b', 3: 'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h', 9:'i'})

    def test_slice_01(self):
        self.assertEqual([1, 2], self.tree.keysinrange(1, 3))

    def test_slice_02(self):
        self.assertEqual([2, 3], self.tree.keysinrange(2, 4))

    def test_slice_03(self):
        self.assertEqual([3, 4, 5], self.tree.keysinrange(2.9, 5.1))

    def test_slice_04(self):
        self.assertEqual([7, 8], self.tree.keysinrange(7, 9))

    def test_slice_no_lower_bound(self):
        self.assertEqual([1, 2], self.tree.keysinrange(None, 3))

    def test_slice_no_upper_bound(self):
        self.assertEqual([6, 7, 8, 9], self.tree.keysinrange(6, None))

    def test_slice_no_bounds(self):
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], self.tree.keysinrange(None, None))

if __name__=='__main__':
    unittest.main()