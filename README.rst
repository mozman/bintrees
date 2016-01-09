Binary Tree Package
===================

Abstract
========

This package provides Binary- RedBlack- and AVL-Trees written in Python and Cython/C.

This Classes are much slower than the built-in *dict* class, but all
iterators/generators yielding data in sorted key order. Trees can be
uses as drop in replacement for *dicts* in most cases.

Source of Algorithms
--------------------

AVL- and RBTree algorithms taken from Julienne Walker: http://eternallyconfuzzled.com/jsw_home.aspx

Trees written in Python
-----------------------

    - *BinaryTree* -- unbalanced binary tree
    - *AVLTree* -- balanced AVL-Tree
    - *RBTree* -- balanced Red-Black-Tree

Trees written with C-Functions and Cython as wrapper
----------------------------------------------------

    - *FastBinaryTree* -- unbalanced binary tree
    - *FastAVLTree* -- balanced AVL-Tree
    - *FastRBTree* -- balanced Red-Black-Tree

All trees provides the same API, the pickle protocol is supported.

Cython-Trees have C-structs as tree-nodes and C-functions for low level operations:

    - insert
    - remove
    - get_value
    - min_item
    - max_item
    - prev_item
    - succ_item
    - floor_item
    - ceiling_item

Constructor
~~~~~~~~~~~

    * Tree() -> new empty tree;
    * Tree(mapping) -> new tree initialized from a mapping (requires only an items() method)
    * Tree(seq) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]

Methods
~~~~~~~

    * __contains__(k) -> True if T has a key k, else False, O(log(n))
    * __delitem__(y) <==> del T[y], del[s:e], O(log(n))
    * __getitem__(y) <==> T[y], T[s:e], O(log(n))
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
    * clear() -> None, remove all items from T, O(n)
    * copy() -> a shallow copy of T, O(n*log(n))
    * discard(k) -> None, remove k from T, if k is present, O(log(n))
    * get(k[,d]) -> T[k] if k in T, else d, O(log(n))
    * is_empty() -> True if len(T) == 0, O(1)
    * items([reverse]) -> generator for (k, v) items of T, O(n)
    * keys([reverse]) -> generator for keys of T, O(n)
    * values([reverse]) -> generator for values of  T, O(n)
    * pop(k[,d]) -> v, remove specified key and return the corresponding value, O(log(n))
    * pop_item() -> (k, v), remove and return some (key, value) pair as a 2-tuple, O(log(n)) (synonym popitem() exist)
    * set_default(k[,d]) -> value, T.get(k, d), also set T[k]=d if k not in T, O(log(n)) (synonym setdefault() exist)
    * update(E) -> None.  Update T from dict/iterable E, O(E*log(n))
    * foreach(f, [order]) -> visit all nodes of tree (0 = 'inorder', -1 = 'preorder' or +1 = 'postorder') and call f(k, v) for each node, O(n)
    * iter_items(s, e[, reverse]) -> generator for (k, v) items of T for s <= key < e, O(n)
    * remove_items(keys) -> None, remove items by keys, O(n)

slicing by keys
~~~~~~~~~~~~~~~

    * item_slice(s, e[, reverse]) -> generator for (k, v) items of T for s <= key < e, O(n), synonym for iter_items(...)
    * key_slice(s, e[, reverse]) -> generator for keys of T for s <= key < e, O(n)
    * value_slice(s, e[, reverse]) -> generator for values of T for s <= key < e, O(n)
    * T[s:e] -> TreeSlice object, with keys in range s <= key < e, O(n)
    * del T[s:e] -> remove items by key slicing, for s <= key < e, O(n)

    start/end parameter:

    * if 's' is None or T[:e] TreeSlice/iterator starts with value of min_key();
    * if 'e' is None or T[s:] TreeSlice/iterator ends with value of max_key();
    * T[:] is a TreeSlice which represents the whole tree;

    The step argument of the regular slicing syntax T[s:e:step] will silently ignored.

    TreeSlice is a tree wrapper with range check and contains no references
    to objects, deleting objects in the associated tree also deletes the object
    in the TreeSlice.

    * TreeSlice[k] -> get value for key k, raises KeyError if k not exists in range s:e
    * TreeSlice[s1:e1] -> TreeSlice object, with keys in range s1 <= key < e1
        - new lower bound is max(s, s1)
        - new upper bound is min(e, e1)

    TreeSlice methods:

    * items() -> generator for (k, v) items of T, O(n)
    * keys() -> generator for keys of T, O(n)
    * values() -> generator for values of  T, O(n)
    * __iter__ <==> keys()
    * __repr__ <==> repr(T)
    * __contains__(key)-> True if TreeSlice has a key k, else False, O(log(n))

prev/succ operations
~~~~~~~~~~~~~~~~~~~~

    * prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))
    * prev_key(key) -> k, get the predecessor of key, O(log(n))
    * succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))
    * succ_key(key) -> k, get the successor of key, O(log(n))
    * floor_item(key) -> get (k, v) pair, where k is the greatest key less than or equal to key, O(log(n))
    * floor_key(key) -> k, get the greatest key less than or equal to key, O(log(n))
    * ceiling_item(key) -> get (k, v) pair, where k is the smallest key greater than or equal to key, O(log(n))
    * ceiling_key(key) -> k, get the smallest key greater than or equal to key, O(log(n))

Heap methods
~~~~~~~~~~~~

    * max_item() -> get largest (key, value) pair of T, O(log(n))
    * max_key() -> get largest key of T, O(log(n))
    * min_item() -> get smallest (key, value) pair of T, O(log(n))
    * min_key() -> get smallest key of T, O(log(n))
    * pop_min() -> (k, v), remove item with minimum key, O(log(n))
    * pop_max() -> (k, v), remove item with maximum key, O(log(n))
    * nlargest(i[,pop]) -> get list of i largest items (k, v), O(i*log(n))
    * nsmallest(i[,pop]) -> get list of i smallest items (k, v), O(i*log(n))

Set methods (using frozenset)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * intersection(t1, t2, ...) -> Tree with keys *common* to all trees
    * union(t1, t2, ...) -> Tree with keys from *either* trees
    * difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
    * symmetric_difference(t1) -> Tree with keys in either T and t1  but not both
    * is_subset(S) -> True if every element in T is in S (synonym issubset() exist)
    * is_superset(S) -> True if every element in S is in T (synonym issuperset() exist)
    * is_disjoint(S) ->  True if T has a null intersection with S (synonym isdisjoint() exist)

Classmethods
~~~~~~~~~~~~

    * from_keys(S[,v]) -> New tree with keys from S and values equal to v. (synonym fromkeys() exist)

Helper functions
~~~~~~~~~~~~~~~~

    * bintrees.has_fast_tree_support() -> True if Cython extension is working else False (False = using pure Python implementation)

Installation
============

from source::

    python setup.py install

or from PyPI::

    pip install bintrees

Compiling the fast Trees requires Cython and on Windows is a C-Compiler necessary (MingW32 works fine, except for
CPython 2.7.10 & CPython 3.5).

Download Binaries for Windows
=============================

http://bitbucket.org/mozman/bintrees/downloads

Documentation
=============

this README.rst

bintrees can be found on bitbucket.org at:

http://bitbucket.org/mozman/bintrees
