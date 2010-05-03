#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary trees package
# Created: 03.05.2010

from random import shuffle

from treemixin import TreeMixin
from bintree import BinaryTree
from avltree import AVLTree
from rbtree import RBTree
from cbintree import cBinaryTree
from cavltree import cAVLTree
from crbtree import cRBTree

__all__ = ['FastBinaryTree', 'FastAVLTree', 'FastRBTree',
           'BinaryTree', 'AVLTree', 'RBTree']

class FastBinaryTree(cBinaryTree, TreeMixin):
    def copy(self):
        """ T.copy() -> a shallow copy of T """
        treekeys = self.keys()
        shuffle(treekeys)  # sorted keys generates a linked list!
        newtree = FastBinaryTree()
        for key in treekeys:
            newtree[key] = self[key]
        return newtree

class FastAVLTree(cAVLTree, TreeMixin):
    def copy(self):
        """ T.copy() -> a shallow copy of T """
        return FastAVLTree(self) # has no problem with sorted keys

class FastRBTree(cRBTree, TreeMixin):
    def copy(self):
        """ T.copy() -> a shallow copy of T """
        return FastRBTree(self) # has no problem with sorted keys
