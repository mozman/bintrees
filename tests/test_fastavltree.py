#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test AVLTrees
# Created: 28.04.2010

import unittest
from tree_test import CheckTree

from bintrees import FastAVLTree

class TestFastAVLTree(CheckTree, unittest.TestCase):
    @property
    def TREE(self):
        return FastAVLTree

if __name__=='__main__':
    unittest.main()