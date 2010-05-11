Binary Tree Package
===================

Abstract
========
This package provides Binary- RedBlack- and AVL-Trees written in Python and Cython.

This Classes are much slower than the built-in dict class, but they have always
sorted keys, and all results of iterators and list returning functions are also sorted.

Source of Algorithms
--------------------
AVL- and RBTree algorithms taken from Julienne Walker: http://eternallyconfuzzled.com/jsw_home.aspx

Trees written in Python (only standard library)
-----------------------------------------------
    - *BinaryTree* -- unbalanced binary tree
    - *AVLTree* -- balanced AVL-Tree
    - *RBTree* -- balanced Red-Black-Tree

Trees written with C-Functions and Cython 0.12.1 as wrapper
-----------------------------------------------------------
    - *FastBinaryTree* -- unbalanced binary tree
    - *FastAVLTree* -- balanced AVL-Tree
    - *FastRBTree* -- balanced Red-Black-Tree

All trees provides the same API, the pickle protocol is supported, but not lambda
functions as user defined compare functions.

FastXTrees has C-structs as tree-node structure and C-implementation for low level
operations: insert, remove, get_value, max_item, min_item, index, item_at.
The biggest performance boost was to use the PyObject_Compare() function from the
C-API as default compare function. If you have to use a user-defined compare
function you will lost this performance advantage.

Constructor
~~~~~~~~~~~
    * Tree([compare]) -> new empty tree, compare(a, b) -> -1, 0, +1; like builtin.cmp
    * Tree(mapping, [compare]) -> new tree initialized from a mapping (requires only a iteritems() method)
    * Tree(seq, [compare]) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]

Methods
~~~~~~~
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
    * clear() -> None, remove all items from T, , O(n)
    * copy() -> a shallow copy of T, O(n*log(n))
    * discard(k) -> None, remove k from T, if k is present, O(log(n))
    * get(k[,d]) -> T[k] if k in T, else d, O(log(n))
    * has_key(k) -> True if T has a key k, else False, O(log(n))
    * is_empty() -> True if len(T) == 0, O(1)
    * items([reverse]) -> list of T's (k, v) pairs, as 2-tuples, O(n)
    * keys([reverse]) -> list of T's keys, O(n)
    * pop(k[,d]) -> v, remove specified key and return the corresponding value, O(log(n))
    * popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple, O(log(n))
    * setdefault(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T, O(log(n))
    * update(E) -> None.  Update T from dict/iterable E, O(E*log(n))
    * values([reverse]) -> list of T's values, O(n)

walk forward/backward
~~~~~~~~~~~~~~~~~~~~~
    * prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))
    * prev_key(key) -> k, get the predecessor of key, O(log(n))
    * succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))
    * succ_key(key) -> k, get the successor of key, O(log(n))

traverse tree
~~~~~~~~~~~~~
    * iteritems([reverse]) -> an iterator over the (k, v) items of T, O(n)
    * iterkeys([reverse]) -> an iterator over the keys of T, O(n)
    * itervalues([reverse]) -> an iterator over the values of T, O(n)
    * treeiter([rtype, reverse]) -> extended TreeIterator (has prev, succ, goto, ... methods)
    * foreach(f, [order]) -> visit all nodes of tree ('inorder', 'preorder' or 'postorder') and call f(k, v) for each node, O(n)

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

Index methods (access by index is slow)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    * index(k) -> index of key k, O(n)
    * item_at(i)-> get (k,v) pair as a 2-tuple at index i, i<0 count from end, O(n)
    * T[s:e:i] -> slicing from start s to end e, step i, O(n)
    * del T[s:e:i] -> remove items by slicing, O(n)

Set methods (using frozenset)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    * intersection(t1, t2, ...) -> Tree with keys *common* to all trees
    * union(t1, t2, ...) -> Tree with keys from *either* trees
    * difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
    * symmetric_difference(t1) -> Tree with keys in either T and t1  but not both
    * issubset(S) -> True if every element in T is in S
    * issuperset(S) -> True if every element in S is in T
    * isdisjoint(S) ->  True if T has a null intersection with S

Classmethods
~~~~~~~~~~~~
    * fromkeys(S[,v]) -> New tree with keys from S and values equal to v.

Performance
===========

Profiling with timeit(): 5000 unique random int keys, time in seconds

BinaryTrees
-----------
========================  =============  ==============  =========
unbalanced BinaryTree     cPython 2.6.5  FastBinaryTree  ipy 2.6.0
========================  =============  ==============  =========
100x build time               7,14           0,40           2,98
100x build & delete time     12,87           1,00           5,04
search 100x all keys          2,96           0,67           1,32
========================  =============  ==============  =========

AVLTrees
--------
========================  =============  =============  =========
AVLTree                   cPython 2.6.5  FastAVLTree    ipy 2.6.0
========================  =============  =============  =========
100x build time             19,51          0,44           10,77
100x build & delete time    32,20          1,05           22,04
search 100x all keys         2,45          0,62            1,31
========================  =============  =============  =========

RBTrees
-------
========================  =============  =============  =========
RBTree                    cPython 2.6.5  FastRBTree     ipy 2.6.0
========================  =============  =============  =========
100x build time             12,41          0,50           5,17
100x build & delete time    35,28          1,23          13,57
search 100x all keys         2,49          0,61           1,35
========================  =============  =============  =========

Memory usage for 100x5000 int keys (Binary/AVL&RB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    * cPython-Trees (20/22) MByte (using __slots__)
    * FastXTrees (20 Bytes/Node on 32 bit systems) x 500.000 = ~9,5 MByte
    * dict 10 MByte

builtin.dict
------------

========================  =============  =========
builtin.dict              cPython 2.6.5  ipy 2.6.0
========================  =============  =========
100x build time             0,03           0,08
100x build & delete time    0,06           0,10
search 100x all keys        0,04           0,04
========================  =============  =========

Installation
============

from source::

    python setup.py install

Download
========
http://bitbucket.org/mozman/bintrees/downloads

Documentation
=============
http://bitbucket.org/mozman/bintrees/wiki/Home

bintrees can be found on bitbucket.org at:

http://bitbucket.org/mozman/bintrees
