#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: avl tree module (Julienne Walker's unbounded none recursive  algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
# Created: 01.05.2010

# Conclusion of Julienne Walker

# AVL trees are about as close to optimal as balanced binary search trees can
# get without eating up resources. You can rest assured that the O(log N)
# performance of binary search trees is guaranteed with AVL trees, but the extra
# bookkeeping required to maintain an AVL tree can be prohibitive, especially
# if deletions are common. Insertion into an AVL tree only requires one single
# or double rotation, but deletion could perform up to O(log N) rotations, as
# in the example of a worst case AVL (ie. Fibonacci) tree. However, those cases
# are rare, and still very fast.

# AVL trees are best used when degenerate sequences are common, and there is
# little or no locality of reference in nodes. That basically means that
# searches are fairly random. If degenerate sequences are not common, but still
# possible, and searches are random then a less rigid balanced tree such as red
# black trees or Andersson trees are a better solution. If there is a significant
# amount of locality to searches, such as a small cluster of commonly searched
# items, a splay tree is theoretically better than all of the balanced trees
# because of its move-to-front design.

from basetree import BaseTree
from array import array

__all__ = ['AVLTree']

MAXSTACK = 32

class Node(object):
    __slots__ = ['left', 'right', 'balance', 'key', 'value']

    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

    def __getitem__(self, key):
        """Get left (==0) or right (==1) node by index"""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """Set left (==0) or right (==1) node by index"""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        """Remove all references."""
        self.left = None
        self.right = None
        self.key = None
        self.value = None

def height(node):
    return node.balance if node is not None else -1

def jsw_single(root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    rlh = height(root.left)
    rrh = height(root.right)
    slh = height(save[other_side])
    root.balance = max(rlh, rrh) + 1
    save.balance = max(slh, root.balance) + 1
    return save

def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)


class AVLTree(BaseTree):
    """AVL Tree (balanced binary search tree)

    The AVL tree structure is a balanced binary tree which stores a collection of
    nodes.  Each node has a key and a value associated with node_stack.  The nodes are
    sorted within the tree based on the order of their keys. Modifications to the
    tree are constructed such that the tree remains balanced at all times (there are
    always roughly equal numbers of nodes on either side of the tree).

    Balanced binary trees have several uses.  They can be used as a mapping
    (searching for a value based on its key), or as a set of keys which is always
    ordered.
    """
    def copy(self):
        """Returns a shallow copy of this tree"""
        return AVLTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        if self.root is None:
            self.root = self.new_node(key, value)
        else:
            node_stack = [] # node stack
            dir_stack = array('I') # direction stack
            done = False
            top = 0
            node = self.root
            # search for an empty link, save path
            while True:
                direction = 1 if self.compare(key, node.key) > 0 else 0
                dir_stack.append(direction)
                node_stack.append(node)
                if node[direction] is None:
                    break
                node = node[direction]

            # Insert a new node at the bottom of the tree
            node[direction] = self.new_node(key, value)

            # Walk back up the search path
            top = len(node_stack) - 1
            while (top >= 0) and not done:
                direction = dir_stack[top]
                other_side = 1 - direction
                topnode = node_stack[top]
                left_height = height(topnode[direction])
                right_height = height(topnode[other_side])

                # Terminate or rebalance as necessary */
                if (left_height-right_height == 0):
                    done = True
                if (left_height-right_height >= 2):
                    a = topnode[direction][direction]
                    b = topnode[direction][other_side]

                    if height(a) >= height(b):
                        node_stack[top] = jsw_single(topnode, other_side)
                    else:
                        node_stack[top] = jsw_double(topnode, other_side)

                    # Fix parent
                    if top != 0:
                        node_stack[top-1][dir_stack[top-1]] = node_stack[top]
                    else:
                        self.root = node_stack[0]
                    done = True

                # Update balance factors
                topnode = node_stack[top]
                left_height = height(topnode[direction])
                right_height = height(topnode[other_side])

                topnode.balance = max(left_height, right_height) + 1
                top -= 1

    def remove(self, key):
        if self.root is None:
            raise KeyError(str(key))
        else:
            compare = self.compare
            node_stack = [None] * MAXSTACK # node stack
            dir_stack = array('I', [0] * MAXSTACK) # direction stack
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
                node = node[direction]
                top += 1

            # Remove the node
            if (node.left is None) or (node.right is None):
                # Which child is not null?
                direction = 1 if node.left is None else 0

                # Fix parent
                if top != 0:
                    node_stack[top-1][dir_stack[top-1]] = node[direction]
                else:
                    self.root = node[direction]
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
                topnode = node_stack[top]
                left_height = height(topnode[direction])
                right_height = height(topnode[other_side])
                b_max = max(left_height, right_height)

                # Update balance factors
                topnode.balance = b_max + 1

                # Terminate or rebalance as necessary
                if (left_height - right_height) == -1:
                    break
                if (left_height - right_height) <= -2:
                    a = topnode[other_side][direction]
                    b = topnode[other_side][other_side]
                    if height(a) <= height(b):
                        node_stack[top] = jsw_single(topnode, direction)
                    else:
                        node_stack[top] = jsw_double(topnode, direction)
                    # Fix parent
                    if top != 0:
                        node_stack[top-1][dir_stack[top-1]] = node_stack[top]
                    else:
                        self.root = node_stack[0]
                top -= 1
