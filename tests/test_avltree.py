#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test AVLTrees
# Created: 28.04.2010

import unittest2 as unittest
from tree_test import TestTreeMixin

from bintrees import AVLTree

class TestAVLTree(TestTreeMixin, unittest.TestCase):
    @property
    def TREE(self):
        return AVLTree

if __name__=='__main__':
    unittest.main()