#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython abstract tree module
# Created: 28.04.2010

from itertools import izip

__all__ = ['cAVLTree']

DEF MAXSTACK = 32

cdef class Node:
    cdef Node left
    cdef Node right
    cdef object key
    cdef object value
    cdef int balance

    def __init__(self, object key=None, object value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

    cdef Node link(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        # this is a little bit faster as __getitem__
        return self.left if key == 0 else self.right

    def __getitem__(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        return self.left if key == 0 else self.right

    def __setitem__(self, int key, Node value):
        """Set left (key==0) or right (key==1) node by index"""
        if key == 0:
            self.left = value
        else:
            self.right = value

    cdef void free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

cdef inline int imax(int a, int b):
    return a if a > b else b

cdef int height(Node node):
    return node.balance if node is not None else -1

cdef Node jsw_single(Node root, int direction):
    cdef Node save
    cdef int other_side
    cdef int rlh, rrh, slh

    other_side = 1 - direction
    save = root.link(other_side)
    root[other_side] = save.link(direction)
    save[direction] = root
    rlh = height(root.left)
    rrh = height(root.right)
    slh = height(save.link(other_side))
    root.balance = imax(rlh, rrh) + 1
    save.balance = imax(slh, root.balance) + 1
    return save

def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)

cdef void tree_to_str(Node node, result):
    if node is not None:
        tree_to_str(node.left, result)
        tree_to_str(node.right, result)
        result.append(repr(node.key)+': '+repr(node.value))

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node.left)
        clear_tree(node.right)
        node.free()

cdef void traverse_inorder(Node node, object func):
    if node is not None:
        traverse_inorder(node.left, func)
        func(node.value)
        traverse_inorder(node.right, func)

cdef void traverse_preorder(Node node, object func):
    if node is not None:
        func(node.value)
        traverse_preorder(node.left, func)
        traverse_preorder(node.right, func)

cdef void traverse_postorder(Node node, object func):
    if node is not None:
        traverse_postorder(node.left, func)
        traverse_postorder(node.right, func)
        func(node.value)

cdef void add_values(Node node, result):
    if node is not None:
        add_values(node.left, result)
        result.append(node.value)
        add_values(node.right, result)

cdef void add_keys(Node node, result):
    if node is not None:
        add_keys(node.left, result)
        result.append(node.key)
        add_keys(node.right, result)

cdef Node get_leaf(Node node):
    while True:
        if node.left is not None:
            node = node.left
        elif node.right is not None:
            node = node.right
        else:
            return node

cdef class cAVLTree:
    cdef Node root
    cdef object compare
    cdef int _count

    def __init__(self, items=[], compare=None):
        self.root = None
        self.compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    def copy(self):
        return cAVLTree(self)

    def __copy__(self):
        return self.copy()

    def __repr__(self):
        result = []
        tree_to_str(self.root, result)
        return "{{{0}}}".format(", ".join(result))

    def has_key(self, key):
        cdef Node node
        node = self.find_node(key)
        return node is not None

    def __contains__(self, key):
        return self.has_key(key)

    def clear(self):
        clear_tree(self.root)
        self._count = 0
        self.root = None

    def __len__(self):
        return self._count

    def is_empty(self):
        return (self.root is None)

    def keys(self):
        result = []
        add_keys(self.root, result)
        return result

    def iterkeys(self):
        return iter(self.keys())

    def __iter__(self):
        return iter(self.keys())

    def values(self):
        result = list()
        add_values(self.root, result)
        return result

    def itervalues(self):
        return iter(self.values())

    def iteritems(self):
        return izip(self.keys(), self.values())

    def items(self):
        return zip(self.keys(), self.values())

    def __getitem__(self, key):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            raise KeyError(unicode(key))
        return node.value

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
        return node.value

    def foreach(self, func, order='inorder'):
        """Visit all tree nodes and process node-value.

        func -- function(node.value)

        order -- 'inorder', 'preorder', 'postorder'
        """
        if order=='inorder':
            traverse_inorder(self.root, func)
        elif order=='postorder':
            traverse_postorder(self.root, func)
        elif order=='preorder':
            traverse_preorder(self.root, func)
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
        tree = cls()
        for key in iterable:
            tree.insert(key, value)
        return tree

    def get(self, key, default=None):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            return default
        else:
            return node.value

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
        value = node.value
        self.remove(key)
        return value

    def popitem(self):
        cdef Node node
        if self.is_empty():
            raise KeyError("popitem(): tree is empty")
        node = get_leaf(self.root)
        result = (node.key, node.value)
        self.remove(node.key)
        return result

    cdef Node find_node(self, object key):
        cdef int cval
        cdef Node node
        compare = self.compare
        node = self.root
        while True:
            if node is None:
                return None
            cval = <int>compare(key, node.key)
            if cval == 0:
                return node
            elif cval < 0:
                node = node.left
            else:
                node = node.right

    cdef Node new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        cdef int dir_stack[MAXSTACK]
        cdef Node node
        cdef int top, direction
        cdef int left_height, right_height
        cdef bint done

        if self.root is None:
            self.root = self.new_node(key, value)
        else:
            node_stack = [] # node stack
            done = False
            top = 0
            node = self.root
            # search for an empty link, save path
            while True:
                direction = 1 if self.compare(key, node.key) > 0 else 0
                dir_stack[top] = direction
                node_stack.append(node)
                if node.link(direction) is None:
                    break
                node = node.link(direction)
                top += 1

            # Insert a new node at the bottom of the tree
            node[direction] = self.new_node(key, value)

            # Walk back up the search path
            top -= 1
            while (top >= 0) and not done:
                direction = dir_stack[top]
                other_side = 1 - direction
                node = <Node> node_stack[top]
                left_height = height(node.link(direction))
                right_height = height(node.link(other_side))

                # Terminate or rebalance as necessary */
                if (left_height-right_height == 0):
                    done = True
                if (left_height-right_height >= 2):
                    node = <Node> node_stack[top]
                    a = node.link(direction).link(direction)
                    b = node.link(direction).link(other_side)

                    if height(a) >= height(b):
                        node_stack[top] = jsw_single(node, other_side)
                    else:
                        node_stack[top] = jsw_double(node, other_side)

                    # Fix parent
                    if top != 0:
                        node = <Node> node_stack[top-1]
                        node[dir_stack[top-1]] = node_stack[top]
                    else:
                        self.root = node_stack[0]
                    done = True

                # Update balance factors
                node = <Node> node_stack[top]
                left_height = height(node.link(direction))
                right_height = height(node.link(other_side))

                node.balance = imax(left_height, right_height) + 1
                top -= 1

    def remove(self, key):
        cdef int dir_stack[MAXSTACK]
        cdef Node node, tmp, heir
        cdef int top, direction, xdir, b_max
        cdef int left_height, right_height
        cdef bint done

        if self.root is None:
            raise KeyError(str(key))
        else:
            compare = self.compare
            node_stack = [None] * MAXSTACK # node stack
            top = 0
            node = self.root

            while True:
                # Terminate if not found
                if node is None:
                    raise KeyError(str(key))
                elif compare(node.key, key)==0:
                    break

                # Push direction and node onto stack
                direction = 1 if compare(key, node.key) > 0 else 0
                dir_stack[top] = direction

                node_stack[top] = node
                node = node.link(direction)
                top += 1

            # Remove the node
            if (node.left is None) or (node.right is None):
                # Which child is not null?
                direction = 1 if node.left is None else 0

                # Fix parent
                if top != 0:
                    tmp = <Node> node_stack[top-1]
                    tmp[dir_stack[top-1]] = node.link(direction)
                else:
                    self.root = node.link(direction)
                node.free()
                self._count -= 1
            else:
                # Find the inorder successor
                heir = node.right

                # Save the path
                dir_stack[top] = 1
                node_stack[top] = node
                top += 1

                while (heir.left is not None):
                    dir_stack[top] = 0
                    node_stack[top] = heir
                    top += 1
                    heir = heir.left

                # Swap data
                node.key = heir.key
                node.value = heir.value

                # Unlink successor and fix parent
                xdir = 1 if compare(node_stack[top-1], node) == 0 else 0
                node_stack[top-1][xdir] = heir.right
                heir.free()
                self._count -= 1

            # Walk back up the search path
            top -= 1
            while top >= 0:
                direction = dir_stack[top]
                other_side = 1 - direction
                node = <Node> node_stack[top]
                left_height = height(node.link(direction))
                right_height = height(node.link(other_side))
                b_max = imax(left_height, right_height)

                # Update balance factors
                node.balance = b_max + 1

                # Terminate or rebalance as necessary
                if (left_height - right_height) == -1:
                    break
                if (left_height - right_height) <= -2:
                    a = node.link(other_side).link(direction)
                    b = node.link(other_side).link(other_side)
                    if height(a) <= height(b):
                        node_stack[top] = jsw_single(node, direction)
                    else:
                        node_stack[top] = jsw_double(node, direction)
                    # Fix parent
                    if top != 0:
                        node_stack[top-1][dir_stack[top-1]] = node_stack[top]
                    else:
                        self.root = node_stack[0]
                top -= 1
