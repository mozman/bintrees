#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: avl tree module (Julienne Walker's unbounded none recursive algorithm)
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
    """ Internal object, represents a treenode """
    __slots__ = ['left', 'right', 'balance', 'key', 'value']
    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

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
    """
    AVLTree implements a balanced binary tree with a dict-like interface.

    see: http://en.wikipedia.org/wiki/AVL_tree

    In computer science, an AVL tree is a self-balancing binary search tree, and
    it is the first such data structure to be invented. In an AVL tree, the
    heights of the two child subtrees of any node differ by at most one;
    therefore, it is also said to be height-balanced. Lookup, insertion, and
    deletion all take O(log n) time in both the average and worst cases, where n
    is the number of nodes in the tree prior to the operation. Insertions and
    deletions may require the tree to be rebalanced by one or more tree rotations.

    The AVL tree is named after its two inventors, G.M. Adelson-Velskii and E.M.
    Landis, who published it in their 1962 paper "An algorithm for the
    organization of information."

    AVLTree([compare=None]) -> new empty tree.
        if compare is None, cmp() is used
        compare(key1, key2) -> -1 if key1 < key2, 0 for key1 == key2 else +1
    AVLTree(mapping, [compare=cmpfunc]) -> new tree initialized from a mapping
        object's (key, value) pairs.
    AVLTree(seq) -> new tree initialized as if via:
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
        T.items() -> list of D's (key, value) pairs, as 2-tuples

    iteritems(...)
        T.iteritems() -> an iterator over the (key, value) items of D

    iterkeys(...)
        T.iterkeys() -> an iterator over the keys of T

    itervalues(...)
        T.itervalues() -> an iterator over the values of T

    keys(...)
        T.keys() -> list of T's keys

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
        T.values() -> list of T's values

    ----------------------------------------------------------------------
    classmethods:

    fromkeys(S[,v])
        AVLTree.fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
        v defaults to None.
    """

    def copy(self):
        """ T.copy() -> a shallow copy of T """
        return AVLTree(self) # has no problem with sorted keys
    __copy__ = copy

    def _new_node(self, key, value):
        """ Create a new treenode """
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """ T.insert(key, value) <==> T[key] = value, insert key, value into Tree """
        if self.root is None:
            self.root = self._new_node(key, value)
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
            node[direction] = self._new_node(key, value)

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
        """ T.remove(key) <==> del T[key], remove item <key> from tree """
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
