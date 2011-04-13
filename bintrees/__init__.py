#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary trees package
# Created: 03.05.2010
# Copyright (C) 2010, 2011 by Manfred Moitzi
# License: GPLv3

from __future__ import absolute_import

"""
Binary Tree Package
===================

Python Trees
------------

Balanced and unbalance binary trees written in pure Python with a dict-like API.

Classes
~~~~~~~
* BinaryTree -- unbalanced binary tree
* AVLTree -- balanced AVL-Tree
* RBTree -- balanced Red-Black-Tree

Cython Trees
------------

Basic tree functions written in Cython, merged with TreeMixin to provide the
full API of the Python Trees.

Classes
~~~~~~~

* FastBinaryTree -- unbalanced binary tree
* FastAVLTree -- balanced AVLTree
* FastRBTree -- balanced Red-Black-Tree

Overview of API for all Classes
===============================

* TreeClass ([compare]) -> new empty tree.
* TreeClass(mapping, [compare]) -> new tree initialized from a mapping
* TreeClass(seq, [compare]) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]

Methods
-------

* __contains__(k) -> True if T has a key k, else False, O(log(n))
* __delitem__(y) <==> del T[y], O(log(n))
* __getitem__(y) <==> T[y], O(log(n))
* __iter__() <==> iter(T)
* __len__() <==> len(T), O(1)
* __max__() <==> max(T), get max item (k,v) of T, O(log(n))
* __min__() <==> min(T), get min item (k,v) of T, O(log(n))
* __and__(other) <==> T & other, intersection
* __or__(other) <==> T | other, union
* __sub__(other) <==> T - other, difference
* __xor__(other) <==> T ^ other, symmetric_difference
* __repr__() <==> repr(T)
* __setitem__(k, v) <==> T[k] = v, O(log(n))
* clear() -> None, Remove all items from T, , O(n)
* copy() -> a shallow copy of T, O(n*log(n))
* discard(k) -> None, remove k from T, if k is present, O(log(n))
* get(k[,d]) -> T[k] if k in T, else d, O(log(n))
* is_empty() -> True if len(T) == 0, O(1)
* items([reverse]) -> list of T's (k, v) pairs, as 2-tuples, O(n)
* keys([reverse]) -> list of T's keys, O(n)
* pop(k[,d]) -> v, remove specified key and return the corresponding value, O(log(n))
* popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple, O(log(n))
* setdefault(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T, O(log(n))
* update(E) -> None.  Update T from dict/iterable E, O(E*log(n))
* values([reverse]) -> list of T's values, O(n)

walk forward/backward, O(log(n))

* prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))
* prev_key(key) -> k, get the predecessor of key, O(log(n))
* succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))
* succ_key(key) -> k, get the successor of key, O(log(n))

traverse tree

* itemslice(startkey, endkey, [reverse]) -> an iterator over the (k, v) items of T for key: startkey <= key < endkey, O(n)
* keyslice(startkey, endkey, [reverse]) -> an iterator over the keys of T for key: startkey <= key < endkey, O(n)
* valueslice(startkey, endkey, [reverse]) -> an iterator over the values of T for key: startkey <= key < endkey, O(n)
* treeiter([rtype, reverse]) -> TreeIterator
* foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node, O(n)

Heap methods

* max_item() -> get biggest (key, value) pair of T, O(log(n))
* max_key() -> get biggest key of T, O(log(n))
* min_item() -> get smallest (key, value) pair of T, O(log(n))
* min_key() -> get smallest key of T, O(log(n))
* pop_min() -> (k, v), remove item with minimum key, O(log(n))
* pop_max() -> (k, v), remove item with maximum key, O(log(n))
* nlargest(i[,pop]) -> get list of i largest items (k, v), O(i*log(n))
* nsmallest(i[,pop]) -> get list of i smallest items (k, v), O(i*log(n))

Index methods (access by index slow)

* index(k) -> index of key k, O(n)
* item_at(i)-> get (k,v) pair as a 2-tuple at index i, i<0 count from end, O(n)
* T[s:e:i] -> slicing from start s to end e, step i, O(n)
* del T[s:e:i] -> remove items by slicing, O(n)

Set methods (using frozenset)

* intersection(t1, t2, ...) -> Tree with keys *common* to all trees
* union(t1, t2, ...) -> Tree with keys from *either* trees
* difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
* symmetric_difference(t1) -> Tree with keys in either T and t1  but not both
* issubset(S) -> True if every element in T is in S
* issuperset(S) -> True if every element in S is in T
* isdisjoint(S) ->  True if T has a null intersection with S

Classmethods

* fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
"""

__all__ = [
    'FastBinaryTree',
    'FastAVLTree',
    'FastRBTree',
    'BinaryTree',
    'AVLTree',
    'RBTree'
]

from .treemixin import TreeMixin
from .iterator import TreeIterator
from .bintree import BinaryTree
from .avltree import AVLTree
from .rbtree import RBTree

try:
    from .qbintree import cBinaryTree
    class FastBinaryTree(cBinaryTree, TreeMixin):
        """ Faster unbalanced binary tree  written in Cython with C-Code. """
except ImportError: # fall back to pure Python version
    FastBinaryTree = BinaryTree
except ValueError: # for pypy
    FastBinaryTree = BinaryTree

try:
    from .qavltree import cAVLTree
    class FastAVLTree(cAVLTree, TreeMixin):
        """ Faster balanced AVL-Tree written in Cython with C-Code. """
except ImportError: # fall back to pure Python version
    FastAVLTree = AVLTree
except ValueError: # for pypy
    FastAVLTree = AVLTree

try:
    from .qrbtree import cRBTree
    class FastRBTree(cRBTree, TreeMixin):
        """ Faster balanced Red-Black-Tree  written in Cython with C-Code. """
except ImportError: # fall back to pure Python version
    FastRBTree = RBTree
except ValueError: # for pypy
    FastRBTree = RBTree
