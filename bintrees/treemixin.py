#!/usr/bin/env python
#coding:utf-8
# Author:  Mozman
# Purpose: treemixin provides top level functions for binary trees
# Created: 03.05.2010
from __future__ import absolute_import

from .iterator import TreeIterator
from .walker import Walker

class TreeMixin(object):
    """
    Abstract-Base-Class for the pure Python Trees: BinaryTree, AVLTree and RBTree
    Mixin-Class for the Cython based Trees: FastBinaryTree, FastAVLTree, FastRBTree

    The TreeMixin Class
    ===================

    T has to implement following properties
    ---------------------------------------

    count -- get node count
    compare -- get compare function, behave like builtin cmp()

    T has to implement following methods
    ------------------------------------
    get_walker(...)
        get a tree walker object, provides methods to traverse the tree see walker.py

    insert(...)
        insert(key, value) <==> T[key] = value, insert key into T

    remove(...)
        remove(key) <==> del T[key], remove key from T

    clear(...)
        T.clear() -> None.  Remove all items from T.

    Methods defined here
    --------------------

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
    * has_key(k) -> True if T has a key k, else False, O(log(n))
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

    * iteritems([reverse]) -> an iterator over the (k, v) items of T, O(n)
    * iterkeys([reverse]) -> an iterator over the keys of T, O(n)
    * itervalues([reverse]) -> an iterator over the values of T, O(n)
    * itemslice(startkey, endkey, [reverse]) -> an iterator over the (k, v) items of T for key: startkey <= key < endkey, O(n)
    * keyslice(startkey, endkey, [reverse]) -> an iterator over the keys of T for key: startkey <= key < endkey, O(n)
    * valueslice(startkey, endkey, [reverse]) -> an iterator over the values of T for key: startkey <= key < endkey, O(n)
    * treeiter([rtype, reverse]) -> extended TreeIterator (has prev, succ, goto, ... methods)
    * foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node, O(n)

    Heap methods

    * max_item() -> get largest (key, value) pair of T, O(log(n))
    * max_key() -> get largest key of T, O(log(n))
    * min_item() -> get smallest (key, value) pair of T, O(log(n))
    * min_key() -> get smallest key of T, O(log(n))
    * pop_min() -> (k, v), remove item with minimum key, O(log(n))
    * pop_max() -> (k, v), remove item with maximum key, O(log(n))
    * nlargest(i[,pop]) -> get list of i largest items (k, v), O(i*log(n))
    * nsmallest(i[,pop]) -> get list of i smallest items (k, v), O(i*log(n))

    Index methods (access by index slow)

    * index(k) -> index of key k, O(n)
    * item_at(i)-> get (k,v) pair as a 2-tuple at index i, i<0 count from end, O(n)
    * T[s:e:i] -> list of (k,v) pairs, from start s to end e, step i, O(n)
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
    def get_walker(self):
        return Walker(self)

    def __repr__(self):
        """ x.__repr__(...) <==> repr(x) """
        def _tostr():
            result = []
            left = None
            right = None
            if node.has_left():
                node.push()
                node.go_left()
                left = _tostr()
                node.pop()
            if node.has_right():
                node.push()
                node.go_right()
                right = _tostr()
                node.pop()
            nodestr = repr(node.key)+': '+repr(node.value)
            if left is not None:
                result.extend(left)
            result.append(nodestr)
            if right is not None:
                result.extend(right)
            return result
        node = self.get_walker()
        if node.is_valid:
            return "{{{0}}}".format(", ".join(_tostr()))
        else:
            return "{}"

    def copy(self):
        """ T.copy() -> get a shallow copy of T. """
        tree = self.__class__(compare=self.compare)
        self.foreach(tree.insert, order=-1)
        return tree
    __copy__ = copy

    def has_key(self, key):
        """ T.has_key(k) -> True if T has a key k, else False """
        return self.get_walker().goto(key)
    __contains__ = has_key

    def __len__(self):
        """ x.__len__() <==> len(x) """
        return self.count

    def __min__(self):
        """ x.__min__() <==> min(x) """
        return self.min_item()

    def __max__(self):
        """ x.__max__() <==> max(x) """
        return self.max_item()

    def __and__(self, other):
        """ x.__and__(other) <==> self & other """
        return self.intersection(other)

    def __or__(self, other):
        """ x.__or__(other) <==> self | other """
        return self.union(other)

    def __sub__(self, other):
        """ x.__sub__(other) <==> self - other """
        return self.difference(other)

    def __xor__(self, other):
        """ x.__xor__(other) <==> self ^ other """
        return self.symmetric_difference(other)

    def discard(self, key):
        """ x.discard(k) -> None, remove k from T, if k is present """
        try:
            self.remove(key)
        except KeyError:
            pass

    def __del__(self):
        self.clear()

    def is_empty(self):
        """ x.is_empty() -> False if T contains any items else True"""
        return self.count == 0

    def keys(self, reverse=False):
        """ T.keys() -> list of T's keys """
        return list(self.iterkeys(reverse))

    def iterkeys(self, reverse=False):
        """ T.iterkeys([reverse]) -> an iterator over the keys of T, in ascending
        order if reverse is True, iterate in descending order, reverse defaults
        to False
        """
        for item in self.iteritems(reverse):
            yield item[0]
    __iter__ = iterkeys

    def treeiter(self, rtype='key', reverse=False):
        """ T.treeiter([rtype, reverse]) -> TreeIterator,
        rtype in ('key', 'value', 'item').
        """
        return TreeIterator(self, rtype, reverse)

    def itemslice(self, startkey, endkey, reverse=False):
        """ T.itemslice(startkey, endkey, [reverse=False]) -> item iterator:
        startkey <= key < endkey.
        """
        def inrange(key):
            return compare(startkey, key) < 1 and compare(key, endkey) < 0

        compare = self.compare
        return ( item for item in self.iteritems(reverse) if inrange(item[0]) )

    def keyslice(self, startkey, endkey, reverse=False):
        """ T.keyslice(startkey, endkey, [reverse=False]) -> key iterator:
        startkey <= key < endkey.
        """
        return ( item[0] for item in self.itemslice(startkey, endkey, reverse) )

    def valueslice(self, startkey, endkey, reverse=False):
        """ T.valueslice(startkey, endkey, [reverse=False]) -> value iterator:
        startkey <= key < endkey.
        """
        return ( item[1] for item in self.itemslice(startkey, endkey, reverse) )

    def __reversed__(self):
        return self.iterkeys(reverse=True)

    def values(self, reverse=False):
        """ T.values() -> list of T's values """
        return list(self.itervalues(reverse))

    def itervalues(self, reverse=False):
        """ T.itervalues([reverse]) -> an iterator over the values of T, in ascending order
        if reverse is True, iterate in descending order, reverse defaults to False
        """
        for item in self.iteritems(reverse):
            yield item[1]

    def iteritems(self, reverse=False):
        """ T.iteritems([reverse]) -> an iterator over the (key, value) items of T,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False
        """
        node = self.get_walker()
        direction = 1 if reverse else 0
        other = 1 - direction
        go_down = True
        while True:
            if node.has_child(direction) and go_down:
                node.push()
                node.down(direction)
            else:
                yield node.item
                if node.has_child(other):
                    node.down(other)
                    go_down = True
                else:
                    if node.stack_is_empty():
                        return # all done
                    node.pop()
                    go_down = False

    def items(self, reverse=False):
        """ T.items() -> list of T's (key, value) pairs, as 2-tuples """
        return list(self.iteritems(reverse))

    def __getitem__(self, key):
        """ x.__getitem__(y) <==> x[y] """
        if isinstance(key, slice):
            return self._slice(key)
        else:
            return self.get_value(key)

    def get_value(self, key):
        node = self.root
        compare = self.compare
        while node is not None:
            cmp_res = compare(key, node.key)
            if cmp_res == 0:
                return node.value
            elif cmp_res < 0:
                node = node.left
            else:
                node = node.right
        raise KeyError(str(key))

    def lower_bound(self, key):
        """ Get first existing key >= key. """
        node = self.get_walker()
        compare = self.compare
        lower_bound = self.max_key()
        if compare(key, lower_bound) > 0:
            raise KeyError(key)

        while node.is_valid:
            nodekey = node.key
            cmp_res = compare(key, nodekey)
            if cmp_res == 0:
                return nodekey
            elif cmp_res < 0:
                if compare(nodekey, lower_bound) < 0:
                    lower_bound = nodekey
                node.go_left()
            else:
                node.go_right()
        return lower_bound

    def upper_bound(self, key):
        """ Get last existing key < key. """
        node = self.get_walker()
        compare = self.compare
        upper_bound = self.min_key()
        if compare(key, upper_bound) < 1:
            raise KeyError(key)

        while node.is_valid:
            nodekey = node.key
            cmp_res = compare(key, nodekey)
            if cmp_res == 0:
                return upper_bound
            elif cmp_res > 0:
                if compare(nodekey, upper_bound) > 0:
                    upper_bound = nodekey
                node.go_right()
            else:
                node.go_left()
        return upper_bound

    def __setitem__(self, key, value):
        """ x.__setitem__(i, y) <==> x[i]=y """
        if isinstance(key, slice):
            raise ValueError('setslice is unsupported')
        self.insert(key, value)

    def __delitem__(self, key):
        """ x.__delitem__(y) <==> del x[y] """
        if isinstance(key, slice):
            self._delslice(key)
        else:
            self.remove(key)

    def __getstate__(self):
        data = dict(self.iteritems())
        return {'data': data, 'cmp': self._compare}

    def __setstate__(self, state):
        self._root = None
        self._count = 0
        self._compare = state['cmp']
        self.update(state['data'])

    def setdefault(self, key, default=None):
        """ T.setdefault(k[,d]) -> T.get(k,d), also set T[k]=d if k not in T """
        walker = self.get_walker()
        if not walker.goto(key):
            self.insert(key, default)
            return default
        return walker.value

    def update(self, *args):
        """ T.update(E) -> None. Update T from E : for (k, v) in E: T[k] = v """
        for items in args:
            try:
                generator = items.iteritems()
            except AttributeError:
                generator = iter(items)

            for key, value in generator:
                self.insert(key, value)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """ T.fromkeys(S[,v]) -> New tree with keys from S and values equal to v.

        v defaults to None.
        """
        tree = cls()
        for key in iterable:
            tree.insert(key, value)
        return tree

    def get(self, key, default=None):
        """ T.get(k[,d]) -> T[k] if k in T, else d.  d defaults to None. """
        walker = self.get_walker()
        if walker.goto(key):
            return walker.value
        else:
            return default

    def pop(self, key, *args):
        """ T.pop(k[,d]) -> v, remove specified key and return the corresponding value
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got {0}".format(
                              1+len(args)))
        walker = self.get_walker()
        if walker.goto(key) is False:
            if len(args) == 0:
                raise KeyError(unicode(key))
            else:
                return args[0]
        value = walker.value
        self.remove(key)
        return value

    def popitem(self):
        """ T.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if T is empty
        """
        if self.is_empty():
            raise KeyError("popitem(): tree is empty")
        walker = self.get_walker()
        walker.goto_leaf()
        result = (walker.key, walker.value)
        self.remove(walker.key)
        return result

    def foreach(self, func, order=0):
        """Visit all tree nodes and process key, value.

        func -- function(key, value)
        order -- inorder = 0, preorder = -1, postorder = +1
        """
        def _traverse():
            if order == -1:
                func(node.key, node.value)
            if node.has_left():
                node.push()
                node.go_left()
                _traverse()
                node.pop()
            if order == 0:
                func(node.key, node.value)
            if node.has_right():
                node.push()
                node.go_right()
                _traverse()
                node.pop()
            if order == +1:
                func(node.key, node.value)

        node = self.get_walker()
        _traverse()

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        walker = self.get_walker()
        if self.count == 0:
            raise ValueError("Tree is empty")
        while walker.has_left():
            walker.go_left()
        return (walker.key, walker.value)

    def pop_min(self):
        """ T.pop_min() -> (k, v), remove item with minimum key, raise KeyError
        if T is empty.
        """
        item = self.min_item()
        self.remove(item[0])
        return item

    def min_key(self):
        """ Get min key of tree, raises ValueError if tree is empty. """
        key, value = self.min_item()
        return key

    def prev_item(self, key):
        """ Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist.
        """
        if self.count == 0:
            raise KeyError("Tree is empty")
        walker = self.get_walker()
        return walker.prev_item(key)

    def succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        if self.count == 0:
            raise KeyError("Tree is empty")
        walker = self.get_walker()
        return walker.succ_item(key)

    def prev_key(self, key):
        """ Get predecessor to key, raises KeyError if key is min key
        or key does not exist.
        """
        key, value = self.prev_item(key)
        return key

    def succ_key(self, key):
        """ Get successor to key, raises KeyError if key is max key
        or key does not exist.
        """
        key, value = self.succ_item(key)
        return key

    def max_item(self):
        """ Get item with max key of tree, raises ValueError if tree is empty. """

        if self.count == 0:
            raise ValueError("Tree is empty")
        walker = self.get_walker()
        while walker.has_right():
            walker.go_right()
        return walker.item

    def pop_max(self):
        """ T.pop_max() -> (k, v), remove item with maximum key, raise KeyError
        if T is empty.
        """
        item = self.max_item()
        self.remove(item[0])
        return item

    def max_key(self):
        """ Get max key of tree, raises ValueError if tree is empty. """
        key, value = self.max_item()
        return key

    def nsmallest(self, n, pop=False):
        """ T.nsmallest(n) -> get list of n smallest items (k, v).
        If pop is True, remove items from T.
        """
        if pop:
            return [self.pop_min() for _ in xrange(min(len(self), n))]
        else:
            gen = self.iterkeys()
            keys = (next(gen) for _ in xrange(min(len(self), n)))
            return [(key, self.get(key)) for key in keys]

    def nlargest(self, n, pop=False):
        """ T.nlargest(n) -> get list of n largest items (k, v).
        If pop is True remove items from T.
        """
        if pop:
            return [self.pop_max() for _ in xrange(min(len(self), n))]
        else:
            gen = self.iterkeys(reverse=True)
            keys = (next(gen) for _ in xrange(min(len(self), n)))
            return [(key, self.get(key)) for key in keys]

    def _slice(self, s):
        """ T._slice(s) -> list of (k,v) pairs, from slice s

        O(n) ... foreach visit all nodes!
        """
        start, end, step = s.indices(self.count)
        reverse = True if start > end else False
        indices = range(start, end, step)
        if len(indices) > 0 :
            if reverse:
                indices = reversed(indices) # indices have to be ascending !!!
            collector = ItemCollector(indices)
            self.foreach(collector.func())
            if reverse:
                return list(reversed(collector.result))
            else:
                return collector.result
        else:
            return []

    def _delslice(self, s):
        """ T._delslice(s) -> remove item from T by slice s

        O(n) ... foreach visit all nodes!
        """
        for key, value in self._slice(s):
            self.remove(key)

    def index(self, key):
        """ T.index(k) -> index, raises KeyError if k not in T """
        node = self.get_walker()
        index = 0
        go_down = True
        while True:
            if node.has_left() and go_down:
                node.push()
                node.go_left()
            else:
                if self.compare(node.key, key) == 0:
                    return index
                index += 1
                if node.has_right():
                    node.go_right()
                    go_down = True
                else:
                    if node.stack_is_empty(): # all done, key not found
                        raise KeyError(str(key))
                    node.pop()
                    go_down = False

    def item_at(self, index):
        """ T.item_at(index) -> item (k,v) """
        if index < 0:
            index = self.count + index
        if (index < 0) or (index >= self.count):
            raise IndexError('item_at()')
        node = self.get_walker()
        counter = 0
        go_down = True
        while True:
            if node.has_left() and go_down:
                node.push()
                node.go_left()
            else:
                if counter == index:
                    return node.item
                counter += 1
                if node.has_right():
                    node.go_right()
                    go_down = True
                else:
                    if node.stack_is_empty():
                        return # all done
                    node.pop()
                    go_down = False

    def intersection(self, *trees):
        """ x.intersection(t1, t2, ...) -> Tree, with keys *common* to all trees
        """
        thiskeys = frozenset(self.iterkeys())
        sets = _make_sets(trees)
        rkeys = thiskeys.intersection(*sets)
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

    def union(self, *trees):
        """ x.union(t1, t2, ...) -> Tree with keys from *either* trees
        """
        thiskeys = frozenset(self.iterkeys())
        sets = _make_sets(trees)
        rkeys = thiskeys.union(*sets)
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

    def difference(self, *trees):
        """ x.difference(t1, t2, ...) -> Tree with keys in T but not any of t1,
        t2, ...
        """
        thiskeys = frozenset(self.iterkeys())
        sets = _make_sets(trees)
        rkeys = thiskeys.difference(*sets)
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

    def symmetric_difference(self, tree):
        """ x.symmetric_difference(t1) -> Tree with keys in either T and t1  but
        not both
        """
        thiskeys = frozenset(self.iterkeys())
        rkeys = thiskeys.symmetric_difference(frozenset(tree.iterkeys()))
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

    def issubset(self, tree):
        """ x.issubset(tree) -> True if every element in x is in tree """
        thiskeys = frozenset(self.iterkeys())
        return thiskeys.issubset(frozenset(tree.iterkeys()))

    def issuperset(self, tree):
        """ x.issubset(tree) -> True if every element in tree is in x """
        thiskeys = frozenset(self.iterkeys())
        return thiskeys.issuperset(frozenset(tree.iterkeys()))

    def isdisjoint(self, tree):
        """ x.isdisjoint(S) ->  True if x has a null intersection with tree """
        thiskeys = frozenset(self.iterkeys())
        return thiskeys.isdisjoint(frozenset(tree.iterkeys()))

def _make_sets(trees):
    sets = []
    for tree in trees:
        sets.append(frozenset(tree.iterkeys()))
    return sets

class KeyIndexer(object):
    """ Get numeric index of keys.
    """
    def __init__(self, keys):
        self.index = 0
        self.keys = frozenset(keys)
        self.result = {} # result[key] = index

    def func(self):
        def _indexer(key, value):
            if key in self.keys:
                self.result[key] = self.index
            self.index += 1
        return _indexer

class ItemCollector(object):
    """Collector object, collect all items defined by numeric indices.
    """
    def __init__(self, indices):
        self.index = 0
        self.wanted = iter(indices)
        self.next_index = self.wanted.next()
        self.result = [] # result list is sorted by key

    def func(self):
        def _collector(key, value):
            if self.index == self.next_index:
                self.result.append( (key, value) )
                try:
                    self.next_index = self.wanted.next()
                except StopIteration:
                    self.next_index = -1
            self.index += 1
        return _collector
