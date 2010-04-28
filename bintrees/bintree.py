#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary tree module
# Created: 28.04.2010

from random import shuffle

from basetree import BaseTree

__all__ = ['BinaryTree']

class TreeNode(object):
    __slots__ = ['key', 'value', 'parent', 'left', 'right']
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.parent = None
        self.value = None
        self.key = None

class BinaryTree(BaseTree):

    def copy(self):
        treekeys = self.keys()
        shuffle(treekeys)  # sorted keys generates a linked list!
        newtree = BinaryTree()
        for key in treekeys:
            newtree[key] = self[key]
        return newtree
    __copy__ = copy

    def __len__(self):
        return self._count

    def new_node(self, key, value, parent):
        """Create a new tree node."""
        self._count += 1
        return TreeNode(key, value, parent)

    def insert(self, key, value):
        if self.root is None:
            self.root = self.new_node(key, value, None)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        cval = self.compare(key, node.key)
        if cval == 0:
            node.value = value
        elif cval < 0:
            if node.left is None:
                node.left = self.new_node(key, value, node)
            else:
                self._insert(node.left, key, value)
        else:
            if node.right is None:
                node.right = self.new_node(key, value, node)
            else:
                self._insert(node.right, key, value)

    def remove(self, key):
        node = self._find_node(self.root, key)
        if node is None:
            raise KeyError(unicode(key))
        else:
            if node.left is None:
                child = node.right
            elif node.right is None:
                child = node.left
            else: #left and right != None
                child = self._smallest_node(node.right)
            self._replace(node, child)
        node.free()
