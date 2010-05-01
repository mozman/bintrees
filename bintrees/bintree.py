#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary tree module
# Created: 28.04.2010

from random import shuffle

from basetree import BaseTree

__all__ = ['BinaryTree']

class Node(object):
    __slots__ = ['key', 'value', 'left', 'right']
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __getitem__(self, key):
        """Get left (==0) or right (==1) node by index"""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """Set left (==0) or right (==1) node by index"""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        self.left = None
        self.right = None
        self.value = None
        self.key = None

def _smallest_node(node):
    while node.left is not None:
        node = node.left
    return node

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

    def new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        if self.root is None:
            self.root = self.new_node(key, value)
        else:
            compare = self.compare
            parent = None
            direction = 0
            node = self.root
            while True:
                if node is None:
                    parent[direction] = self.new_node(key, value)
                    break
                cval = compare(key, node.key)
                if cval == 0: # key exists
                    node.value = value # replace value
                    break
                else:
                    parent = node
                    direction = 0 if cval < 0 else 1
                    node = node[direction]

    def remove(self, key):
        node = self.root
        if node is None:
            return
        else:
            compare = self.compare
            parent = None
            direction = 0
            while True:
                cmp_res = compare(key, node.key)
                if cmp_res == 0:
                    if (node.left is not None) and (node.right is not None):
                        child = _smallest_node(node.right)
                        #swap places
                        child.key, node.key = node.key, child.key
                        child.value, node.value = node.value, child.value
                        parent = node
                        direction = 1
                        node = node.right
                        continue
                    else:
                        down_dir = 1 if node.left is None else 0
                        if parent is None: # root
                            self.root = node[down_dir]
                        else:
                            parent[direction] = node[down_dir]
                    node.free()
                    self._count -= 1
                    break
                else:
                    direction = 0 if cmp_res < 0 else 1
                    parent = node
                    node = node[direction]
                    if node is None:
                        raise KeyError(str(key))
