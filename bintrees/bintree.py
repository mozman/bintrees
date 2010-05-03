#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary tree module
# Created: 28.04.2010

from random import shuffle

from treemixin import TreeMixin

__all__ = ['BinaryTree']

class Node(object):
    """ Internal object, represents a treenode """
    __slots__ = ['key', 'value', 'left', 'right']
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __getitem__(self, key):
        """ x.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right) """
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """ x.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right) """
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        """ Set references to None """
        self.left = None
        self.right = None
        self.value = None
        self.key = None

class BinaryTree(TreeMixin):
    """
    BinaryTree implements an unbalanced binary tree with a dict-like interface.

    see: http://en.wikipedia.org/wiki/Binary_tree

    A binary tree is a tree data structure in which each node has at most two
    children.

    BinaryTree([compare=None]) -> new empty tree.
        if compare is None, cmp() is used
        compare(key1, key2) -> -1 if key1 < key2, 0 for key1 == key2 else +1
    BinaryTree(mapping, [compare=cmpfunc]) -> new tree initialized from a mapping
        object's (key, value) pairs.
    BinaryTree(seq) -> new tree initialized as if via:
        for k, v in seq:
            T[k] = v

    Methods defined here:
    __contains__(...)
        T.__contains__(k) -> True if T has a key k, else False

    __delitem__(...)
        x.__delitem__(y) <==> del x[y]

    __getitem__(...)
        x.__getitem__(y) <==> x[y]

    __init__(...)
        x.__init__(...) initializes x; see x.__class__.__doc__ for signature

    __iter__(...)
        x.__iter__() <==> iter(x)

    __len__(...)
        x.__len__() <==> len(x)

    __repr__(...)
        x.__repr__() <==> repr(x)

    __setitem__(...)
        x.__setitem__(i, y) <==> x[i]=y

    clear(...)
        T.clear() -> None.  Remove all items from T.

    copy(...)
        T.copy() -> a shallow copy of T

    foreach(...)
        T.foreach(self, func, order) -> visit all nodes of tree and call
        func(key, value) at each node.

        order -- 'preorder', 'inorder', 'postorder'
            'preorder' -- func(), traverse left-subtree, traverse right-subtree
            'inorder' -- traverse left-subtree, func(), traverse right-subtree
            'postorder' -- traverse left-subtree, traverse right-subtree, func()

    get(...)
        T.get(k[,d]) -> T[k] if k in T, else d.  d defaults to None.

    has_key(...)
        T.has_key(k) -> True if T has a key k, else False

    insert(key, value)
        T.insert(key, value) <==> T[key] = value, insert key, value into Tree

    is_empty(...)
        T.is_empty() -> True if len(T) == 0

    items(...)
        T.items([reverse]) -> list of T's (key, value) pairs, as 2-tuples in
        ascending order, if reverse is True, in descending order, reverse
        defaults to False

    iteritems(...)
        T.iteritems([reverse]) -> an iterator over the (key, value) items of T,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False

    iterkeys(...)
        T.iterkeys([reverse]) -> an iterator over the keys of T, in ascending order
        if reverse is True, iterate in descending order, reverse defaults to False

    itervalues(...)
        T.itervalues([reverse]) -> an iterator over the values of T, in ascending order
        if reverse is True, iterate in descending order, reverse defaults to False

    keys(...)
        T.keys([reverse]) -> list of T's keys in ascending order, if reverse is
        True, in descending order, reverse defaults to False

    max_item(...)
        T.max_item() -> get biggest (key, value) pair of T

    max_key(...)
        T.max_key() -> get biggest key of T

    min_item(...)
        T.min_item() -> get smallest (key, value) pair of T

    min_key(...)
        T.min_key() -> get smallest key of T

    nlargest(...)
        T.nlargest(n[,pop]) -> get list of n largest items (k, v)
        If pop is True remove items from T, pop defaults to False

    nsmallest(...)
        T.nlargest(n[,pop]) -> get list of n smallest items (k, v)
        If pop is True remove items from T, pop defaults to False

    pop(...)
        T.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised

    popitem(...)
        T.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if T is empty.

    pop_min(...)
        T.pop_min() -> (k, v), remove item with minimum key, raise KeyError if T
        is empty.

    pop_max(...)
        T.pop_max() -> (k, v), remove item with maximum key, raise KeyError if T
        is empty.

    prev_item(...)
        T.prev_item(key) -> get (k, v) pair, where k is predecessor to key

    prev_key(...)
        T.prev_key(key) -> k, get the predecessor of key

    remove(...)
        T.remove(key) <==> del T[key], remove item <key> from tree

    setdefault(...)
        T.setdefault(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T

    succ_item(...)
        T.succ_item(key) -> get (k, v) pair, where k is successor to key

    succ_key(...)
        T.succ_key(key) -> k, get the successor of key

    update(...)
        T.update(E) -> None.  Update T from dict/iterable E.
        If E has a .iteritems() method, does: for (k, v) in E: T[k] = v
        If E lacks .iteritems() method, does: for (k, v) in iter(E): T[k] = v

    values(...)
        T.values([reverse]) -> list of T's values in ascending order, if reverse
        is True, in descending order, reverse defaults to False

    ----------------------------------------------------------------------
    classmethods:

    fromkeys(S[,v])
        BinaryTree.fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
        v defaults to None.
    """
    def __init__(self, items=[], compare=None):
        """ x.__init__(...) initializes x; see x.__class__.__doc__ for signature """
        self._root = None
        self._compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    def clear(self):
        """ T.clear() -> None.  Remove all items from T. """
        def _clear(node):
            if node is not None:
                _clear(node.left)
                _clear(node.right)
                node.free()
        _clear(self._root)
        self._count = 0
        self._root = None

    @property
    def count(self):
        return self._count

    @property
    def root(self):
        return self._root

    @property
    def compare(self):
        return self._compare

    def copy(self):
        """ T.copy() -> a shallow copy of T """
        treekeys = self.keys()
        shuffle(treekeys)  # sorted keys generates a linked list!
        newtree = BinaryTree()
        for key in treekeys:
            newtree[key] = self[key]
        return newtree
    __copy__ = copy

    def _new_node(self, key, value):
        """ Create a new tree node. """
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """ T.insert(key, value) <==> T[key] = value, insert key, value into Tree """
        if self._root is None:
            self._root = self._new_node(key, value)
        else:
            compare = self._compare
            parent = None
            direction = 0
            node = self._root
            while True:
                if node is None:
                    parent[direction] = self._new_node(key, value)
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
        """ T.remove(key) <==> del T[key], remove item <key> from tree """
        node = self._root
        if node is None:
            raise KeyError(str(key))
        else:
            compare = self._compare
            parent = None
            direction = 0
            while True:
                cmp_res = compare(key, node.key)
                if cmp_res == 0:
                    # remove node
                    if (node.left is not None) and (node.right is not None):
                        # find replacment node: smallest key in right-subtree
                        parent = node
                        direction = 1
                        replacement = node.right
                        while replacement.left is not None:
                            parent = replacement
                            direction = 0
                            replacement = replacement.left
                        parent[direction] = replacement.right
                        #swap places
                        node.key = replacement.key
                        node.value = replacement.value
                        node = replacement # delete replacement!
                    else:
                        down_dir = 1 if node.left is None else 0
                        if parent is None: # root
                            self._root = node[down_dir]
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
