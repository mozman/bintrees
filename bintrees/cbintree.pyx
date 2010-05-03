#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010

from itertools import izip
from random import shuffle

__all__ = ['cBinaryTree']

cdef class Node:
    cdef Node _left
    cdef Node _right
    cdef object _key
    cdef object _value

    def __init__(self, key, value):
        self._left = None
        self._right = None
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key
    @property
    def value(self):
        return self._value
    @property
    def item(self):
        return (self._key, self._value)
    @property
    def left(self):
        return self._left
    @property
    def right(self):
        return self._right

    cdef Node link(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        # this is a little bit faster as __getitem__
        return self._left if key == 0 else self._right

    def __getitem__(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        return self._left if key == 0 else self._right

    def __setitem__(self, int key, Node value):
        """Set left (key==0) or right (key==1) node by index
        """
        if key == 0:
            self._left = value
        else:
            self._right = value

    cdef void free(self):
        self._left = None
        self._right = None
        self._key = None
        self._value = None

cdef void tree_to_str(Node node, result):
    if node is not None:
        tree_to_str(node._left, result)
        tree_to_str(node._right, result)
        result.append(repr(node._key)+': '+repr(node._value))

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node._left)
        clear_tree(node._right)
        node.free()

cdef void traverse_inorder(Node node, object func):
    if node is not None:
        traverse_inorder(node._left, func)
        func(node._key, node._value)
        traverse_inorder(node._right, func)

cdef void traverse_preorder(Node node, object func):
    if node is not None:
        func(node._key, node._value)
        traverse_preorder(node._left, func)
        traverse_preorder(node._right, func)

cdef void traverse_postorder(Node node, object func):
    if node is not None:
        traverse_postorder(node._left, func)
        traverse_postorder(node._right, func)
        func(node._key, node._value)

cdef void add_values(Node node, result):
    if node is not None:
        add_values(node._left, result)
        result.append(node._value)
        add_values(node._right, result)

cdef void add_keys(Node node, result):
    if node is not None:
        add_keys(node._left, result)
        result.append(node._key)
        add_keys(node._right, result)

cdef Node get_leaf(Node node):
    while True:
        if node._left is not None:
            node = node._left
        elif node._right is not None:
            node = node._right
        else:
            return node

cdef class cBinaryTree:
    cdef Node _root
    cdef object compare
    cdef int _count

    def __init__(self, items=[], compare=None):
        self._root = None
        self.compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    @property
    def root(self):
        return self._root

    def copy(self):
        cdef cBinaryTree newtree
        cdef Node node
        treekeys = self._keys()
        shuffle(treekeys)  # sorted keys generates a linked list!
        newtree = cBinaryTree()
        for key in treekeys:
            node = self.find_node(key)
            newtree.insert(key, node._value)
        return newtree

    def get_root(self):
        return self._root

    def __copy__(self):
        return self.copy()

    def __repr__(self):
        result = []
        tree_to_str(self._root, result)
        return "{{{0}}}".format(", ".join(result))

    def has_key(self, key):
        cdef Node node
        node = self.find_node(key)
        return node is not None

    def __contains__(self, key):
        return self.has_key(key)

    def clear(self):
        clear_tree(self._root)
        self._count = 0
        self._root = None

    def __len__(self):
        return self._count

    def is_empty(self):
        return (self._root is None)

    def keys(self):
        result = []
        add_keys(self._root, result)
        return result

    def iterkeys(self):
        return iter(self._keys())

    def __iter__(self):
        return iter(self._keys())

    def values(self):
        result = list()
        add_values(self._root, result)
        return result

    def itervalues(self):
        return iter(self._values())

    def iteritems(self):
        return izip(self._keys(), self._values())

    def items(self):
        return zip(self._keys(), self._values())

    def __getitem__(self, key):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            raise KeyError(unicode(key))
        return node._value

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def setdefault(self, key, default=None):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            self.insert(key, default)
            return default
        return node._value

    def foreach(self, func, order='inorder'):
        """Visit all tree nodes and process node-value.

        func -- function(node._value)

        order -- 'inorder', 'preorder', 'postorder'
        """
        if order=='inorder':
            traverse_inorder(self._root, func)
        elif order=='postorder':
            traverse_postorder(self._root, func)
        elif order=='preorder':
            traverse_preorder(self._root, func)
        else:
            raise ValueError("foreach(): unknown order '{0}'.".format(order))

    def update(self, items):
        try:
            generator = items.iteritems()
        except AttributeError:
            generator = iter(items)

        for key, value in generator:
            self.insert(key, value)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        cdef cBinaryTree tree
        tree = cBinaryTree()
        for key in iterable:
            tree.insert(key, value)
        return tree

    def get(self, key, default=None):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            return default
        else:
            return node._value

    def pop(self, key, *args):
        cdef Node node
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got {0}".format(
                              1+len(args)))

        node = self.find_node(key)
        if node is None:
            if len(args) == 0:
                raise KeyError(unicode(key))
            else:
                return args[0]
        value = node._value
        self.remove(key)
        return value

    def popitem(self):
        cdef Node node
        if self._root is None:
            raise KeyError("popitem(): tree is empty")
        node = get_leaf(self._root)
        result = (node._key, node._value)
        self.remove(node._key)
        return result

    cdef Node find_node(self, object key):
        cdef int cval
        cdef Node node
        compare = self.compare
        node = self._root
        while True:
            if node is None:
                return None
            cval = <int>compare(key, node._key)
            if cval == 0:
                return node
            elif cval < 0:
                node = node._left
            else:
                node = node._right

    cdef Node new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return Node(key, value)

    cpdef insert(self, key, value):
        cdef Node parent, node
        cdef int direction, cval

        if self._root is None:
            self._root = self.new_node(key, value)
        else:
            compare = self.compare
            direction = 0
            parent = None
            node = self._root
            while True:
                if node is None:
                    parent[direction] = self.new_node(key, value)
                    break
                cval = <int> compare(key, node._key)
                if cval == 0: # key exists
                    node._value = value # replace value
                    break
                else:
                    parent = node
                    direction = 0 if cval < 0 else 1
                    node = node.link(direction)

    cpdef remove(self, key):
        cdef Node node, parent, replacement
        cdef int direction, cmp_res, down_dir

        node = self._root
        if node is None:
            raise KeyError(str(key))
        else:
            compare = self.compare
            parent = None
            direction = 0
            while True:
                cmp_res = <int> compare(key, node._key)
                if cmp_res == 0:
                    # remove node
                    if (node._left is not None) and (node._right is not None):
                        # find replacment node: smallest key in right-subtree
                        parent = node
                        direction = 1
                        replacement = node._right
                        while replacement._left is not None:
                            parent = replacement
                            direction = 0
                            replacement = replacement._left
                        parent[direction] = replacement._right
                        #swap places
                        node._key = replacement._key
                        node._value = replacement._value
                        node = replacement # delete replacement node
                    else:
                        down_dir = 1 if node._left is None else 0
                        if parent is None: # root
                            self._root = node.link(down_dir)
                        else:
                            parent[direction] = node.link(down_dir)
                    node.free()
                    self._count -= 1
                    break
                else:
                    direction = 0 if cmp_res < 0 else 1
                    parent = node
                    node = node.link(direction)
                    if node is None:
                        raise KeyError(str(key))
