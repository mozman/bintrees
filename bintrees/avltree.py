#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: avl tree module (Julienne Walker Recursive Algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
# unbounded top-down algorithm
# Created: 01.05.2010

# Conclusion of Julian Walker

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
    rlh = height(root[0])
    rrh = height(root[1])
    slh = height(save[other_side])
    root.balance = max(rlh, rrh) + 1
    save.balance = max(slh, root.balance) +1
    return save

def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)


class AVLTree(BaseTree):
    """AVL Tree (balanced binary search tree)

    The AVL tree structure is a balanced binary tree which stores a collection of
    nodes.  Each node has a key and a value associated with it.  The nodes are
    sorted within the tree based on the order of their keys. Modifications to the
    tree are constructed such that the tree remains balanced at all times (there are
    always roughly equal numbers of nodes on either side of the tree).

    Balanced binary trees have several uses.  They can be used as a mapping
    (searching for a value based on its key), or as a set of keys which is always
    ordered.
    """
    def __init__(self, items=[], compare=None):
        BaseTree.__init__(self, items, compare)
        self._done = True

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
            up = []
            upd = []
            done = False
            top = 0
            node = self.root
            # search for an empty link, save path
            while True:
                direction = 1 if self.compare(key, node.key) > 0 else 0
                upd.append(direction)
                up.append(node)
                if node[direction] is None:
                    break
                node = node[direction]

            # Insert a new node at the bottom of the tree
            node[direction] = self.new_node(key, value)

            # Walk back up the search path
            top = len(up) - 1
            while (top >= 0) and not done:
                direction = upd[top]
                lh = height(up[top][direction])
                rh = height(up[top][1-direction])

                # Terminate or rebalance as necessary */
                if (lh-rh == 0):
                    done = True
                if (lh-rh >= 2):
                    a = up[top][direction][direction]
                    b = up[top][direction][1-direction]

                    if height(a) >= height(b):
                        up[top] = jsw_single(up[top], 1-direction)
                    else:
                        up[top] = jsw_double(up[top], 1-direction)

                    # Fix parent
                    if top != 0:
                        up[top-1][upd[top-1]] = up[top]
                    else:
                        self.root = up[0]
                    done = True

                # Update balance factors
                lh = height(up[top][direction])
                rh = height(up[top][1-direction])

                up[top].balance = max(lh, rh) + 1
                top -= 1

    def remove(self, key):
        if self.root is not None:
            compare = self.compare
            up = [None] * MAXSTACK
            upd = [0] * MAXSTACK
            top = 0
            it = self.root

            while True:
                # Terminate if not found
                if it is None:
                    raise KeyError(str(key))
                elif compare(it.key, key)==0:
                    break

                # Push direction and node onto stack
                direction = 1 if compare(key, it.key) > 0 else 0
                upd[top] = direction

                up[top] = it
                it = it[direction]
                top += 1

            # Remove the node
            if (it.left is None) or (it.right is None):
                # Which child is not null?
                direction = 1 if it.left is None else 0

                # Fix parent
                if top != 0:
                    up[top-1][upd[top-1]] = it[direction]
                else:
                    self.root = it[direction]
                it.free()
                self._count -= 1
            else:
                # Find the inorder successor
                heir = it[1]

                # Save the path
                upd[top] = 1
                up[top] = it
                top += 1

                while (heir[0] is not None):
                    upd[top] = 0
                    up[top] = heir
                    top += 1
                    heir = heir[0]

                # Swap data
                it.key = heir.key
                it.value = heir.value

                # Unlink successor and fix parent
                xdir = 1 if compare(up[top-1], it) == 0 else 0
                up[top-1][xdir] = heir[1]
                heir.free()
                self._count -= 1

            # Walk back up the search path
            top -= 1
            while top >= 0:
                lh = height(up[top][upd[top]])
                rh = height(up[top][1-upd[top]])
                b_max = max(lh, rh)

                # Update balance factors
                up[top].balance = b_max + 1

                # Terminate or rebalance as necessary
                if (lh - rh) == -1:
                    break
                if (lh - rh) <= -2:
                    a = up[top][1-upd[top]][upd[top]]
                    b = up[top][1-upd[top]][1-upd[top]]
                    if height(a) <= height(b):
                        up[top] = jsw_single(up[top], upd[top])
                    else:
                        up[top] = jsw_double(up[top], upd[top])
                    # Fix parent
                    if top != 0:
                        up[top-1][upd[top-1]] = up[top]
                    else:
                        self.root = up[0]
                top -= 1
