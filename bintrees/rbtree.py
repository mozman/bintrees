#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: red-black tree module (Julienne Walker Top-down Algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
# Created: 01.05.2010

from basetree import BaseTree

__all__ = ['RBTree']

class Node(object):
    __slots__ = ['key', 'value', 'red', 'left', 'right']
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.red = True
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

    def __getitem__(self, key):
        """Get left or right node by index"""
        if key == 0:
            return self.left
        elif key == 1:
            return self.right
        else:
            raise KeyError(str(key))

    def __setitem__(self, key, value):
        """Set left or right node by index"""
        if key == 0:
            self.left = value
        elif key == 1:
            self.right = value
        else:
            raise KeyError(str(key))

def is_red(node):
    if (node is not None) and node.red:
        return True
    else:
        return False

def jsw_single (root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    root.red = True
    save.red = False
    return save

def jsw_double (root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)

class RBTree(BaseTree):
    def copy(self):
        return RBTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        # does not work !?
        compare = self.compare
        if self.root is None: # Empty tree case
            self.root = self.new_node(key, value)
            self.root.red = False # make root black
            return

        head = Node() # False tree root
        grandparent = None # Grandparent
        t = head # parent
        p = None # Iterator
        direction = 0
        last = 0

        # Set up helpers
        t[1] = self.root
        q = t[1]
        # Search down the tree
        while True:
            if (q is None):# Insert new node at the bottom
                q = self.new_node(key, value)
                p[direction] = q
            elif is_red(q[0]) and is_red(q[1]):# Color flip
                q.red = True
                q[0].red = False
                q[1].red = False

            # Fix red violation
            if is_red(q) and is_red(p):
                direction2 = int(t[1] is grandparent)
                if q is p[last]:
                    t[direction2] = jsw_single(grandparent, 1-last)
                else:
                    t[direction2] = jsw_double(grandparent, 1-last)

            # Stop if found
            cmp_res = compare(key, q.key)
            if cmp_res == 0:
                q.value = value #set new value for key
                break

            last = direction
            if cmp_res < 0:
                direction = 0 # key < q.key
            else:
                direction = 1 # key > q.key

            # Update helpers
            if grandparent is not None:
                t = grandparent
            grandparent = p
            p = q
            q = q[direction]

        self.root = head[1] # Update root
        self.root.red = False # make root black

    def remove(self, key):
        compare = self.compare
        if self.root is None:
            return
        head = Node() # False tree root
        node = head
        node.right = self.root
        parent = None
        grandparent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while (node[direction] is not None):
            last = direction

            # Update helpers
            grandparent = parent
            parent = node
            node = node[direction]
            direction = int(compare(node.key, key) < 0)

            # Save found node
            if compare(node.key, key) == 0:
                found = node

            # Push the red node down
            if (not is_red(node)) and (not is_red(node[direction])):
                if is_red(node[1-direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                elif not is_red(node[1-direction]):
                    s = parent[1-last]
                    if s is not None:
                        if (not is_red(s[1-last])) and (not is_red(s[last])):
                            # Color flip
                            parent.red = False
                            s.red = True
                            node.red = True
                        else:
                            direction2 = int(grandparent.right == parent)
                            if is_red(s[last]):
                                grandparent[direction2] = jsw_double(parent, last)
                            elif is_red(s[1-last]):
                                grandparent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            node.red = grandparent[direction2].red = True
                            grandparent[direction2].left.red = False
                            grandparent[direction2].right.red = False

        # Replace and remove if found
        if found is not None:
            found.key = node.key
            found.value = node.value
            parent[int(parent.right == node)] = node[int(node.left == None)]
            node.free()
            self._count -= 1

        # Update root and make it black
        self.root = head.right
        if self.root is not None:
            self.root.red = False
