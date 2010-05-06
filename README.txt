Binary Tree Package
===================

Abstract
========
This package provides Binary- RedBlack- and AVL-Trees written in Python and Cython.

This Classes are much slower than the bulitin.dict class and uses twice as much memory, but
they have always sorted keys, and all results of iterators and list returning functions are also sorted.

All trees provides the same API.

If you looking for a really fast RBTree see also http://pypi.python.org/pypi/rbtree written by Benjamin Saller.
His rbtree class is 3x .. 4x times faster than my FastRBTree class.

Source of Algorithms
--------------------
AVL- and RBTree algorithms taken from Julienne Walker: http://eternallyconfuzzled.com/jsw_home.aspx

Trees written in Python (only standard library)
-----------------------------------------------
    - *BinaryTree* -- unbalanced binary tree
    - *AVLTree* -- balanced AVL-Tree
    - *RBTree* -- balanced Red-Black-Tree

Trees written in Cython 0.12.1
------------------------------
    - *FastBinaryTree* -- unbalanced binary tree
    - *FastAVLTree* -- balanced AVL-Tree
    - *FastRBTree* -- balanced Red-Black-Tree

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

Profiling with timeit(): 5000 unique random keys, time in seconds

BinartyTrees
------------
========================  =============  =============  =========
unbalanced BinaryTree     cPython 2.6.5  Cython 0.12.1  ipy 2.6.0
========================  =============  =============  =========
100x build time               6,85           0,90          2,85
100x build & delete time     12,55           1,88          5,09
search 100x all keys          2,91           0,67          1,35
========================  =============  =============  =========

AVLTrees
--------
========================  =============  =============  =========
AVLTree                   cPython 2.6.5  Cython 0.12.1  ipy 2.6.0
========================  =============  =============  =========
100x build time             18,33          1,50           11,45
100x build & delete time    31,50          3,54           23,07
search 100x all keys         2,33          1,03           1,33
========================  =============  =============  =========

RBTrees
-------
========================  =============  =============  =========  =========
RBTree                    cPython 2.6.5  Cython 0.12.1  ipy 2.6.0  bcsaller
========================  =============  =============  =========  =========
100x build time             12,63          1,13           5,27      0,54
100x build & delete time    35,37          2,90          13,73      0,89
search 100x all keys         2,53          1,14           1,35      0,36
========================  =============  =============  =========  =========

builtin.dict
------------

*dict* is a really, really fast datatype, and it uses also less than half of the memory:

Memory usage for 100x5000 keys (Binary/AVL&RB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	* cPython-Trees (20/22) MByte
	* Cython-Trees (22/24) MByte
	* dict 10 MByte

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

Binary packages for 32-bit Win and Linux will be available on http://bitbucket.org/mozman/bintrees/downloads

Documentation
=============
http://bitbucket.org/mozman/bintrees/wiki/Home

bintrees can be found on bitbucket.org at:

http://bitbucket.org/mozman/bintrees
