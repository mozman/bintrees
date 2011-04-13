#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: DEPRICATED FastBinaryTree
# Created: 28.04.2010
# Copyright (C) 2010, 2011 by Manfred Moitzi
# License: GPLv3
# no longer maintained

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

    def free(self):
        self._left = None
        self._right = None
        self._key = None
        self._value = None

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node.left)
        clear_tree(node.right)
        node.free()

cdef class cBinaryTree:
    cdef Node _root
    cdef int _count
    cdef object _compare

    def __init__(self, items=[], compare=None):
        self._root = None
        self._compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    @property
    def root(self):
        return self._root

    @property
    def compare(self):
        return self._compare

    @property
    def count(self):
        return self._count

    cdef Node new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return Node(key, value)

    def clear(self):
        clear_tree(self._root)
        self._count = 0
        self._root = None

    def get_value(self, key):
        cdef int cval
        cdef Node node
        node = self._root
        while node is not None:
            cval = <int>self._compare(key, node._key)
            if cval == 0:
                return node._value
            elif cval < 0:
                node = node._left
            else:
                node = node._right
        raise KeyError(str(key))

    def insert(self, key, value):
        cdef Node parent, node
        cdef int direction, cval

        if self._root is None:
            self._root = self.new_node(key, value)
        else:
            compare = self._compare
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

    def remove(self, key):
        cdef Node node, parent, replacement
        cdef int direction, cmp_res, down_dir

        node = self._root
        if node is None:
            raise KeyError(str(key))
        else:
            compare = self._compare
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

    def prev_item(self, key):
        """ Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist.
        """
        cdef Node node, prev
        cdef int cval

        node = self._root
        if node is None:
            raise KeyError("Tree is empty")
        prev = None
        while node is not None:
            cval = <int>self._compare(key, node._key)
            if cval == 0:
                break
            elif cval < 0:
                node = node._left
            else:
                if (prev is None) or (<int>self._compare(node._key, prev._key) > 0):
                    prev = node
                node = node._right

        if node is None:
            raise KeyError(unicode(key))
        # found node of key
        if node._left is not None:
            # find biggest node of left subtree
            node = node._left
            while node._right is not None:
                node = node._right
            if prev is None:
                prev = node
            elif <int>self._compare(node._key, prev._key) > 0:
                prev = node
        elif prev is None: # given key is smallest in tree
            raise KeyError(unicode(key))
        return (prev._key, prev._value)

    def succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        cdef Node node, succ
        cdef int cval

        node = self._root
        if node is None:
            raise KeyError("Tree is empty")
        succ = None
        while node is not None:
            cval = <int>self._compare(key, node._key)
            if cval == 0:
                break
            elif cval < 0:
                if (succ is None) or (<int>self._compare(node._key, succ._key) < 0):
                    succ = node
                node = node._left
            else:
                node = node._right

        if node is None:
            raise KeyError(unicode(key))
        # found node of key
        if node._right is not None:
            # find smallest node of right subtree
            node = node._right
            while node._left is not None:
                node = node._left
            if succ is None:
                succ = node
            elif <int>self._compare(node._key, succ._key) < 0:
                succ = node
        elif succ is None: # given key is biggest in tree
            raise KeyError(unicode(key))
        return (succ._key, succ._value)

    def max_item(self):
        """ Get item with max key of tree, raises ValueError if tree is empty. """
        cdef Node node
        node = self._root
        if node is None: # root is None
            raise ValueError("Tree is empty")
        while node._right is not None:
            node = node._right
        return (node._key, node._value)

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        cdef Node node
        node = self._root
        if node is None: # root is None
            raise ValueError("Tree is empty")
        while node._left is not None:
            node = node._left
        return (node._key, node._value)

    def index(self, key):
        """ T.index(k) -> index, raises KeyError if k not in T """
        cdef Node node
        cdef int index
        cdef bint go_down

        node = self._root
        index = 0
        go_down = True
        stack = list()
        while True:
            if node._left is not None and go_down:
                stack.append(node)
                node = node._left
            else:
                if <int>self._compare(node._key, key) == 0:
                    return index
                index += 1
                if node._right is not None:
                    node = node._right
                    go_down = True
                else:
                    if not len(stack):
                        raise KeyError(str(key))
                    node = stack.pop()
                    go_down = False

    def item_at(self, int index):
        """ T.item_at(index) -> item (k,v) """
        cdef Node node
        cdef int counter
        cdef bint go_down

        if index < 0:
            index = self._count + index
        if (index < 0) or (index >= self._count):
            raise IndexError('item_at()')
        node = self._root
        counter = 0
        go_down = True
        stack = list()
        while True:
            if node._left is not None and go_down:
                stack.append(node)
                node = node._left
            else:
                if counter == index:
                    return (node._key, node._value)
                counter += 1
                if node._right is not None:
                    node = node._right
                    go_down = True
                else:
                    if not len(stack):
                        return # all done
                    node = stack.pop()
                    go_down = False
