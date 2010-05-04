#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary trees package
# Created: 03.05.2010
"""
Binary Tree Package
===================

Python Trees
------------

Balanced and unbalance binary trees written in pure Python with a dict-like API.

Classes
-------
 * BinaryTree -- unbalanced binary tree
 * AVLTree -- balanced AVL-Tree
 * RBTree -- balanced Red-Black-Tree

Cython Trees
------------

Basic tree functions written in Cython, merged with TreeMixin to  provide the
full API of the Python Trees.

Classes
-------

 * FastBinaryTree -- unbalanced binary tree
 * FastAVLTree -- balanced AVLTree
 * FastRBTree -- balanced Red-Black-Tree

Overview of API for all Classes
===============================

 * TreeClass ([compare]) -> new empty tree.
 * TreeClass(mapping, [compare]) -> new tree initialized from a mapping
 * TreeClass(seq, [compare]) -> new tree initialized from seq

Methods
-------

 * __contains__(k) -> True if T has a key k, else False
 * __delitem__(y) <==> del T[y]
 * __getitem__(y) <==> T[y]
 * __iter__() <==> iter(T)
 * __len__() <==> len(T)
 * __repr__() <==> repr(T)
 * __setitem__(k, v) <==> T[k] = v
 * clear() -> None, Remove all items from T.
 * copy() -> a shallow copy of T
 * foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node.
 * get(k[,d]) -> T[k] if k in T, else d
 * has_key(k) -> True if T has a key k, else False
 * insert(k, v) <==> T[k] = v, insert k, v into T
 * is_empty() -> True if len(T) == 0
 * items([reverse]) -> list of T's (k, v) pairs, as 2-tuples
 * iteritems([reverse]) -> an iterator over the (k, v) items of T.
 * iterkeys([reverse]) -> an iterator over the keys of T
 * itervalues([reverse]) -> an iterator over the values of T
 * keys([reverse]) -> list of T's keys
 * max_item() -> get biggest (key, value) pair of T
 * max_key() -> get biggest key of T
 * min_item() -> get smallest (key, value) pair of T
 * min_key() -> get smallest key of T
 * nlargest(n[,pop]) -> get list of n largest items (k, v)
 * nsmallest(n[,pop]) -> get list of n smallest items (k, v)
 * pop(k[,d]) -> v, remove specified key and return the corresponding value.
 * popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple
 * pop_min() -> (k, v), remove item with minimum key
 * pop_max() -> (k, v), remove item with maximum key
 * prev_item(key) -> get (k, v) pair, where k is predecessor to key
 * prev_key(key) -> k, get the predecessor of key
 * remove(k) <==> del T[k], remove item k from T
 * setdefault(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T
 * succ_item(key) -> get (k, v) pair, where k is successor to key
 * succ_key(key) -> k, get the successor of key
 * update(E) -> None.  Update T from dict/iterable E.
 * values([reverse]) -> list of T's values

Classmethods
------------

 * fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
"""

from random import shuffle

from treemixin import TreeMixin
from iterator import TreeIterator
from bintree import BinaryTree
from avltree import AVLTree
from rbtree import RBTree
from cbintree import cBinaryTree
from cavltree import cAVLTree
from crbtree import cRBTree

__all__ = ['FastBinaryTree', 'FastAVLTree', 'FastRBTree',
           'BinaryTree', 'AVLTree', 'RBTree']

class FastBinaryTree(cBinaryTree, TreeMixin):
    """ Fast unbalanced binary tree. """
    def copy(self):
        """ T.copy() -> a shallow copy of T """
        treekeys = self.keys()
        shuffle(treekeys)  # sorted keys generates a linked list!
        newtree = FastBinaryTree()
        for key in treekeys:
            newtree[key] = self[key]
        return newtree

class FastAVLTree(cAVLTree, TreeMixin):
    """ Fast balanced AVL-Tree. """
    def copy(self):
        """ T.copy() -> a shallow copy of T """
        return FastAVLTree(self) # has no problem with sorted keys

class FastRBTree(cRBTree, TreeMixin):
    """ Fast balanced Red-Black-Tree. """
    def copy(self):
        """ T.copy() -> a shallow copy of T """
        return FastRBTree(self) # has no problem with sorted keys
