
NEWS
====

Version 2.0.7 - 2017-04-28

  * BUGFIX: foreach (pure Python implementation) works with empty trees
  * acquire GIL for PyMem_Malloc() and PyMem_Free() calls

Version 2.0.6 - 2017-02-04

  * BUGFIX: correct deepcopy() for tree in tree

Version 2.0.5 - 2017-02-04

  * support for copy.deepcopy()
  * changed status back to `Mature`, there will be: bugfixes, compatibility checks and simple additions like this deep
    copy support, because I got feedback, that there are some special cases in which `bintrees` can be useful.
  * switched development to 64bit only & MS compilers - on Windows 7 everything works fine now with CPython 2.7/3.5/3.6

Repository moved to GitHub: https://github.com/mozman/bintrees.git

Version 2.0.4 - 2016-01-09

  * removed logging statements on import
  * added helper function bintrees.has_fast_tree_support()
  * HINT: pypy runs faster than CPython with Cython extension

Version 2.0.3 - 2016-01-06

  * replaced print function by logging.warning for import warning messages
  * KNOWN ISSUE: unable to build Cython extension with MingW32 and CPython 3.5 & CPython 2.7.10

Version 2.0.2 - 2015-02-12

  * fixed foreach cython-function by Sam Yaple

Version 2.0.1 - 2013-10-01

  * removed __del__() method to avoid problems with garbage collection

Version 2.0.0 - 2013-06-01

  * API change: consistent method naming with synonyms for dict/set compatibility
  * code base refactoring
  * removed tree walkers
  * removed low level node stack implementation -> caused crashes
  * optimizations for pypy: iter_items(), succ_item(), prev_item()
  * tested with CPython2.7, CPython3.3, pypy-2.0 on Win7 and Linux Mint 15 x64 (pypy-1.9)

Version 1.0.3 - 2013-05-01

  * extended iter_items(startkey=None, endkey=None, reverse=reverse) -> better performance for slicing
  * Cython implementation of iter_items() for Fast_X_Trees()
  * added key parameter *reverse* to itemslice(), keyslice(), valueslice()
  * tested with CPython2.7, CPython3.3, pypy-2.0

Version 1.0.2 - 2013-04-01

  * bug fix: FastRBTree data corruption on inserting existing keys
  * bug fix: union & symmetric_difference - copy all values to result tree

Version 1.0.1 - 2013-02-01

  * bug fixes
  * refactorings by graingert
  * skip useless tests for pypy
  * new license: MIT License
  * tested with CPython2.7, CPython3.2, CPython3.3, pypy-1.9, pypy-2.0-beta1
  * unified line endings to LF
  * PEP8 refactorings
  * added floor_item/key, ceiling_item/key methods, thanks to Dai Mikurube

Version 1.0.0 - 2011-12-29

  * bug fixes
  * status: 5 - Production/Stable
  * removed useless TreeIterator() class and T.treeiter() method.
  * patch from Max Motovilov to use Visual Studio 2008 for building C-extensions

Version 0.4.0 - 2011-04-14

  * API change!!!
  * full Python 3 support, also for Cython implementations
  * removed user defined compare() function - keys have to be comparable!
  * removed T.has_key(), use 'key in T'
  * keys(), items(), values() generating 'views'
  * removed iterkeys(), itervalues(), iteritems() methods
  * replaced index slicing by key slicing
  * removed index() and item_at()
  * repr() produces a correct representation
  * installs on systems without cython (tested with pypy)
  * new license: GNU Library or Lesser General Public License (LGPL)

Version 0.3.2 - 2011-04-09

  * added itemslice(startkey, endkey), keyslice(startkey, endkey),
    valueslice(startkey, endkey) - slicing by keys
  * tested with pypy 1.4.1, damn fast
  * Pure Python trees are working with Python 3
  * No Cython implementation for Python 3

Version 0.3.1 - 2010-09-10

  * runs with Python 2.7

Version 0.3.0 - 2010-05-11

  * low level functions written as c-module only interface to python is a cython
    module
  * support for the pickle protocol

Version 0.2.1 - 2010-05-06

  * added delslice del T[0:3] -> remove treenodes 0, 1, 2
  * added discard -> remove key without KeyError if not found
  * added heap methods: min, max, nlarges, nsmallest ...
  * added Set methods -> intersection, differnce, union, ...
  * added slicing: T[5:10] get items with position (not key!)  5, 6, 7, 8, 9
          T[5] get item with key! 5
  * added index: T.index(key) -> get position of item <key>
  * added item_at: T.item_at(0) -> get item at position (not key!) 0
          T.item_at(0) O(n)! <==> T.min_item() O(log(n))

Version 0.2.0 - 2010-05-03

  * TreeMixin Class as base for Python-Trees and as Mixin for Cython-Trees

Version 0.1.0 - 2010-04-27

  * Alpha status
  * Initial release
