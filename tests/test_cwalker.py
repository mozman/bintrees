#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test the tree walker class
# Created: 08.05.2010

import unittest
from walker_test import WalkerCheck
from bintrees import FastBinaryTree

testkeys = [10, 5, 15, 3, 7, 12, 20, 1, 4, 6, 8, 30]
testitems = list(zip(testkeys, testkeys))

class TestWalker(WalkerCheck, unittest.TestCase):
    def get_tree(self, items):
        return FastBinaryTree(items)

if __name__=='__main__':
    unittest.main()