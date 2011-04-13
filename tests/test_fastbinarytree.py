#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test fast binary trees
# Created:03.05.2010

import unittest
from tree_test import CheckTree

from bintrees import FastBinaryTree

class TestFastBinaryTree(CheckTree, unittest.TestCase):
    @property
    def TREE(self):
        return FastBinaryTree

if __name__=='__main__':
    unittest.main()