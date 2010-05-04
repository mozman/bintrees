#!/usr/bin/env python
#coding:utf-8
# Author:  Mozman
# Purpose: treemixin provides top level functions for binary trees
# Created: 03.05.2010

from iterator import TreeIterator

class TreeMixin(object):
    """
    Abstract-Base-Class for the pure Python Trees: BinaryTree, AVLTree and RBTree
    Mixin-Class for the Cython based Trees: FastBinaryTree, FastAVLTree, FastRBTree

    The Node Class
    ==============

    N has to implement following properties
    ---------------------------------------

        key -- get key object of node
        value -- get value object of node
        left -- get left node
        right -- get right node

    N has to implement following methods
    ------------------------------------

    free(...)
        N.free() set all object references to None

    __getitem__(...)
        N.__getitem(n) <==> N[0] or N[1]
        N[0] get left node of N, N[1] get right node of N

    The TreeMixin Class
    ===================

    T has to implement following properties
    ---------------------------------------

    root -- get root node
    count -- get node count
    compare -- get compare function, behave like builtin cmp()

    T has to implement following methods
    ------------------------------------
    insert(...)
        insert(key, value) <==> T[key] = value, insert key into T

    remove(...)
        remove(key) <==> del T[key], remove key from T

    clear(...)
        T.clear() -> None.  Remove all items from T.

    Methods
    -------

    * __contains__(k) -> True if T has a key k, else False
    * __delitem__(y) <==> del T[y]
    * __getitem__(y) <==> T[y]
    * __iter__() <==> iter(T)
    * __len__() <==> len(T)
    * __max__() <==> max(T), get max item (k,v) of T
    * __min__() <==> min(T), get min item (k,v) of T
    * __repr__() <==> repr(T)
    * __setitem__(k, v) <==> T[k] = v
    * clear() -> None, Remove all items from T.
    * copy() -> a shallow copy of T
    * discard(k) -> None, remove k from T, if k is present
    * get(k[,d]) -> T[k] if k in T, else d
    * has_key(k) -> True if T has a key k, else False
    * is_empty() -> True if len(T) == 0
    * items([reverse]) -> list of T's (k, v) pairs, as 2-tuples
    * keys([reverse]) -> list of T's keys
    * pop(k[,d]) -> v, remove specified key and return the corresponding value.
    * popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple
    * setdefault(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T
    * update(E) -> None.  Update T from dict/iterable E.
    * values([reverse]) -> list of T's values

    walk forward/backward (not really fast!)

    * prev_item(key) -> get (k, v) pair, where k is predecessor to key
    * prev_key(key) -> k, get the predecessor of key
    * succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key
    * succ_key(key) -> k, get the successor of key

    traverse tree

    * iteritems([reverse]) -> an iterator over the (k, v) items of T.
    * iterkeys([reverse]) -> an iterator over the keys of T
    * itervalues([reverse]) -> an iterator over the values of T
    * treeiter([rtype, reverse]) -> TreeIterator
    * foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node.

    Heap methods

    * max_item() -> get biggest (key, value) pair of T
    * max_key() -> get biggest key of T
    * min_item() -> get smallest (key, value) pair of T
    * min_key() -> get smallest key of T
    * pop_min() -> (k, v), remove item with minimum key
    * pop_max() -> (k, v), remove item with maximum key
    * nlargest(n[,pop]) -> get list of n largest items (k, v)
    * nsmallest(n[,pop]) -> get list of n smallest items (k, v)

    Index methods (access by index is slow!)

    * index_of(k) -> index of key k
    * item_at(i)-> get (k,v) pair as a 2-tuple at index i, i<0 count from end
    * T[s:e:i] -> slicing from start s to end e, step i

    Set methods

    * intersection(t1, t2, ...) -> Tree with keys *common* to all trees
    * union(t1, t2, ...) -> Tree with keys from *either* trees
    * difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
    * symetric_difference(t1) -> Tree with keys in either T and t1  but not both

    Classmethods

    * fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
    """

    def _get_leaf(self):
        """ get a leaf node """
        node = self.root
        while node is not None:
            if node.left is not None:
                node = node.left
            elif node.right is not None:
                node = node.right
            else:
                return node
        return None

    def find_node(self, key):
        """ T.find_node(key) -> get treenode of key, returns None if not found.
        """
        node = self.root
        compare = self.compare
        while node is not None:
            cval = compare(key, node.key)
            if cval == 0:
                return node
            elif cval < 0:
                node = node.left
            else:
                node = node.right
        return None

    def __repr__(self):
        """ x.__repr__(...) <==> repr(x) """
        def _tostr(node):
            if node is not None:
                result = []
                left = _tostr(node.left)
                right = _tostr(node.right)
                nodestr = repr(node.key)+': '+repr(node.value)
                if left is not None:
                    result.extend(left)
                result.append(nodestr)
                if right is not None:
                    result.extend(right)
                return result
            else:
                return None
        return "{{{0}}}".format(", ".join(_tostr(self.root)))

    def __copy__(self):
        """ T.__copy__() -> get a shallow copy of T. """
        return self.copy()

    def has_key(self, key):
        """ T.has_key(k) -> True if T has a key k, else False """
        node = self.find_node(key)
        return node is not None
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

    def discard(self, key):
        """ x.discard(k) -> None, remove k from T, if k is present """
        try:
            self.remove(key)
        except KeyError:
            pass

    def is_empty(self):
        """ x.is_empty() -> False if T contains any items else True"""
        return self.root is None

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
        """ T.treeiter([rtype, reverse]) -> TreeIterator """
        return TreeIterator(self)

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
        node = self.root
        direction = 1 if reverse else 0
        other = 1 - direction
        go_down = True
        stack = list()
        while True:
            if node[direction] is not None and go_down:
                stack.append(node)
                node = node[direction]
            else:
                yield (node.key, node.value)
                if node[other] is not None:
                    node = node[other]
                    go_down = True
                else:
                    if not len(stack):
                        return # all done
                    node = stack.pop()
                    go_down = False

    def items(self, reverse=False):
        """ T.items() -> list of T's (key, value) pairs, as 2-tuples """
        return list(self.iteritems(reverse))

    def __getitem__(self, key):
        """ x.__getitem__(y) <==> x[y] """
        # overwrite this in cython
        if isinstance(key, slice):
            return self._slice(key)
        else:
            node = self.find_node(key)
            if node is None:
                raise KeyError(unicode(key))
            return node.value

    def __setitem__(self, key, value):
        """ x.__setitem__(i, y) <==> x[i]=y """
        self.insert(key, value)

    def __delitem__(self, key):
        """ x.__delitem__(y) <==> del x[y] """
        self.remove(key)

    def setdefault(self, key, default=None):
        """ T.setdefault(k[,d]) -> T.get(k,d), also set T[k]=d if k not in T """
        node = self.find_node(key)
        if node is None:
            self.insert(key, default)
            return default
        return node.value

    def update(self, items):
        """ T.update(E) -> None. Update T from E : for (k, v) in E: T[k] = v """
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
        node = self.find_node(key)
        if node is None:
            return default
        else:
            return node.value

    def pop(self, key, *args):
        """ T.pop(k[,d]) -> v, remove specified key and return the corresponding value
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got {0}".format(
                              1+len(args)))
        node = self.find_node(key)
        if node is None:
            if len(args) == 0:
                raise KeyError(unicode(key))
            else:
                return args[0]
        value = node.value
        self.remove(key)
        return value

    def popitem(self):
        """ T.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if T is empty
        """
        if self.is_empty():
            raise KeyError("popitem(): tree is empty")
        node = self._get_leaf()
        result = (node.key, node.value)
        self.remove(node.key)
        return result

    def foreach(self, func, order='inorder'):
        """Visit all tree nodes and process key, value.

        func -- function(key, value)
        order -- 'inorder', 'preorder', 'postorder' default is 'inorder'
        """
        def _traverse_inorder(node):
            if node is None: return
            _traverse_inorder(node.left)
            func(node.key, node.value)
            _traverse_inorder(node.right)

        def _traverse_preorder(node):
            if node is None: return
            func(node.key, node.value)
            _traverse_preorder(node.left)
            _traverse_preorder(node.right)

        def _traverse_postorder(node):
            if node is None: return
            _traverse_postorder(node.left)
            _traverse_postorder(node.right)
            func(node.key, node.value)

        if order=='inorder':
            _traverse_inorder(self.root)
        elif order=='postorder':
            _traverse_postorder(self.root)
        elif order=='preorder':
            _traverse_preorder(self.root)
        else:
            raise ValueError("foreach(): unknown order '{0}'.".format(order))

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        node = self.root
        if node is None: # root is None
            raise ValueError("Tree is empty")
        while node.left is not None:
            node = node.left
        return (node.key, node.value)

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
        node = self.root
        if node is None:
            raise KeyError("tree is empty")
        path = []
        compare = self.compare
        while node is not None:
            cval = compare(key, node.key)
            if cval == 0:
                break
            elif cval < 0:
                node = node.left
            else:
                path.append(node) # predecessor on path to root?
                node = node.right

        if node is None:
            raise KeyError(unicode(key))
        # found node of key
        if node.left is not None:
            # find biggest node of left subtree
            node = node.left
            while node.right is not None:
                node = node.right
            path.append(node)
        else: # left subtree is None
            if len(path) == 0: # given key is smallest in tree
                raise KeyError(unicode(key))

        # find max key on stack
        nodes = iter(path)
        node = next(nodes)
        for pathnode in nodes: # contains only nodes which are < key
            if compare(pathnode.key, node.key) > 0:
                node = pathnode
        return (node.key, node.value)

    def succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        node = self.root
        if node is None:
            raise KeyError("Tree is empty")
        path = []
        compare = self.compare
        while node is not None:
            cval = compare(key, node.key)
            if cval == 0:
                break
            elif cval < 0:
                path.append(node) # successor on path to root?
                node = node.left
            else:
                node = node.right

        if node is None:
            raise KeyError(unicode(key))
        # found node of key
        if node.right is not None:
            # find smallest node of right subtree
            node = node.right
            while node.left is not None:
                node = node.left
            path.append(node)
        else: # right subtree is None
            if len(path) == 0: # given key is biggest in tree
                raise KeyError(unicode(key))

        # find min key on stack
        nodes = iter(path)
        node = next(nodes)
        for pathnode in nodes: # contains only nodes which are > key
            if compare(pathnode.key, node.key) < 0:
                node = pathnode
        return (node.key, node.value)

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
        node = self.root
        if node is None: # root is None
            raise ValueError("Tree is empty")
        while node.right is not None:
            node = node.right
        return (node.key, node.value)

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
        """ T.slice(s) -> list of (k,v) pairs, from slice s

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

    def index_of(self, key):
        """ T.index_of(k) -> index, raises KeyError if k not in T

        O(n) ... foreach visit all nodes!
        """
        indexer = KeyIndexer( (key,) )
        self.foreach(indexer.func())
        return indexer.result[key]

    def item_at(self, index):
        """ T.item_at(index) -> item (k,v)

        O(n) ... foreach visit all nodes!
        """
        if index < 0:
            index = self.count + index
        if 0 <= index < self.count:
            collector = ItemCollector( (index,) )
            self.foreach(collector.func())
            return collector.result[0]
        else:
            return None

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
        rkeys = thiskeys.intersection(*sets)
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

    def difference(self, *trees):
        """ x.difference(t1, t2, ...) -> Tree with keys in T but not any of t1,
        t2, ...
        """
        thiskeys = frozenset(self.iterkeys())
        sets = _make_sets(trees)
        rkeys = thiskeys.difference(*sets)
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

    def symetric_difference(self, tree):
        """ x.symetric_difference(t1) -> Tree with keys in either T and t1  but
        not both
        """
        thiskeys = frozenset(self.iterkeys())
        rkeys = thiskeys.symmetric_difference(frozenset(tree))
        return self.__class__( ((key, self.get(key)) for key in rkeys) )

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

