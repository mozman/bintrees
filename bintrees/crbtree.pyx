#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: DEPRICATED FastRBTree
# Created: 28.04.2010
# Copyright (C) 2010, 2011 by Manfred Moitzi
# License: GPLv3
# no longer maintained

__all__ = ['cRBTree']

cdef class Node:
    cdef Node _left
    cdef Node _right
    cdef object _key
    cdef object _value
    cdef bint red

    def __init__(self, object key=None, object value=None):
        self._left = None
        self._right = None
        self._key = key
        self._value = value
        self.red = True

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
        """Set left (key==0) or right (key==1) node by index"""
        if key == 0:
            self._left = value
        else:
            self._right = value

    def free(self):
        self._left = None
        self._right = None
        self._key = None
        self._value = None

cdef bint is_red(Node node):
    if (node is not None) and node.red:
        return True
    else:
        return False

cdef Node jsw_single(Node root, int direction):
    cdef int other_side
    cdef Node save

    other_side = 1 - direction
    save = root.link(other_side)
    root[other_side] = save.link(direction)
    save[direction] = root
    root.red = True
    save.red = False
    return save

cdef Node jsw_double(Node root, int direction):
    cdef int otherside
    other_side = 1 - direction
    root[other_side] = jsw_single(root.link(other_side), other_side)
    return jsw_single(root, direction)

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node._left)
        clear_tree(node._right)
        node.free()


cdef class cRBTree:
    cdef Node _root
    cdef object _compare
    cdef int _count

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
        cdef Node head, grand_grand_parent, grand_parent, parent, node
        cdef int direction, direction2, last, cmp_res

        compare = self._compare
        if self._root is None: # Empty tree case
            self._root = self.new_node(key, value)
            self._root.red = False # make root black
            return

        head = Node() # False tree root
        grand_parent = None # Grandparent
        grand_grand_parent = head # parent
        parent = None # Iterator
        direction = 0
        last = 0

        # Set up helpers
        grand_grand_parent._right = self._root
        node = grand_grand_parent._right
        # Search down the tree
        while True:
            if node is None: # Insert new node at the bottom
                node = self.new_node(key, value)
                parent[direction] = node
            elif is_red(node._left) and is_red(node._right):# Color flip
                node.red = True
                node._left.red = False
                node._right.red = False

            # Fix red violation
            if is_red(node) and is_red(parent):
                direction2 = 1 if grand_grand_parent._right is grand_parent else 0
                if node is parent.link(last):
                    grand_grand_parent[direction2] = jsw_single(grand_parent, 1-last)
                else:
                    grand_grand_parent[direction2] = jsw_double(grand_parent, 1-last)

            # Stop if found
            cmp_res = compare(key, node._key)
            if cmp_res == 0:
                node._value = value #set new value for key
                break

            last = direction
            direction = 0 if cmp_res < 0 else 1
            # Update helpers
            if grand_parent is not None:
                grand_grand_parent = grand_parent
            grand_parent = parent
            parent = node
            node = node.link(direction)

        self._root = head._right # Update root
        self._root.red = False # make root black

    def remove(self, key):
        cdef Node head, node, parent, grand_parent, found, sibling
        cdef int direction, last, direction2, cmp_res

        if self._root is None:
            raise KeyError(str(key))
        compare = self._compare
        head = Node() # False tree root
        node = head
        node._right = self._root
        parent = None
        grand_parent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while (node.link(direction) is not None):
            last = direction

            # Update helpers
            grand_parent = parent
            parent = node
            node = node.link(direction)
            cmp_res = compare(key, node._key)
            direction = 1 if cmp_res > 0 else 0

            # Save found node
            if cmp_res == 0:
                found = node

            # Push the red node down
            if (not is_red(node)) and (not is_red(node.link(direction))):
                if is_red(node.link(1-direction)):
                    parent[last] = jsw_single(node, direction)
                    parent = parent.link(last)
                elif not is_red(node.link(1-direction)):
                    sibling = parent.link(1-last)
                    if sibling is not None:
                        if (not is_red(sibling.link(1-last))) and \
                           (not is_red(sibling.link(last))):
                            # Color flip
                            parent.red = False
                            sibling.red = True
                            node.red = True
                        else:
                            direction2 = 1 if grand_parent._right is parent else 0
                            if is_red(sibling.link(last)):
                                grand_parent[direction2] = jsw_double(parent, last)
                            elif is_red(sibling.link(1-last)):
                                grand_parent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            grand_parent.link(direction2).red = True
                            node.red = True
                            grand_parent.link(direction2)._left.red = False
                            grand_parent.link(direction2)._right.red = False

        # Replace and remove if found
        if found is not None:
            found._key = node._key
            found._value = node._value
            direction = 1 if parent._right is node else 0
            direction2 = 1 if node._left is None else 0
            parent[direction] = node.link(direction2)
            node.free()
            self._count -= 1

        # Update root and make it black
        self._root = head._right
        if self._root is not None:
            self._root.red = False
        if not found:
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
