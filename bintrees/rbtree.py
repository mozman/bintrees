#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: red-black tree module (Julienne Walker's none recursive algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
# Created: 01.05.2010

# Conclusion of Julian Walker

# Red black trees are interesting beasts. They're believed to be simpler than
# AVL trees (their direct competitor), and at first glance this seems to be the
# case because insertion is a breeze. However, when one begins to play with the
# deletion algorithm, red black trees become very tricky. However, the
# counterweight to this added complexity is that both insertion and deletion
# can be implemented using a single pass, top-down algorithm. Such is not the
# case with AVL trees, where only the insertion algorithm can be written top-down.
# Deletion from an AVL tree requires a bottom-up algorithm.

# So when do you use a red black tree? That's really your decision, but I've
# found that red black trees are best suited to largely random data that has
# occasional degenerate runs, and searches have no locality of reference. This
# takes full advantage of the minimal work that red black trees perform to
# maintain balance compared to AVL trees and still allows for speedy searches.

# Red black trees are popular, as most data structures with a whimsical name.
# For example, in Java and C++, the library map structures are typically
# implemented with a red black tree. Red black trees are also comparable in
# speed to AVL trees. While the balance is not quite as good, the work it takes
# to maintain balance is usually better in a red black tree. There are a few
# misconceptions floating around, but for the most part the hype about red black
# trees is accurate.

from basetree import BaseTree

__all__ = ['RBTree']

class Node(object):
    """ Internal object, represents a treenode """
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
        """ x.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right) """
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """ x.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right) """
        if key == 0:
            self.left = value
        else:
            self.right = value

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
    """
    RBTree implements a balanced binary tree with a dict-like interface.

    see: http://en.wikipedia.org/wiki/Red_black_tree

    A red-black tree is a type of self-balancing binary search tree, a data
    structure used in computing science, typically used to implement associative
    arrays. The original structure was invented in 1972 by Rudolf Bayer, who
    called them "symmetric binary B-trees", but acquired its modern name in a
    paper in 1978 by Leonidas J. Guibas and Robert Sedgewick. It is complex,
    but has good worst-case running time for its operations and is efficient in
    practice: it can search, insert, and delete in O(log n) time, where n is
    total number of elements in the tree. Put very simply, a red-black tree is a
    binary search tree which inserts and removes intelligently, to ensure the
    tree is reasonably balanced.

    RBTree([compare=None]) -> new empty tree.
        if compare is None, cmp() is used
        compare(key1, key2) -> -1 if key1 < key2, 0 for key1 == key2 else +1
    RBTree(mapping, [compare=cmpfunc]) -> new tree initialized from a mapping
        object's (key, value) pairs.
    RBTree(seq) -> new tree initialized as if via:
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
        RBTree.fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
        v defaults to None.
    """

    def copy(self):
        """ T.copy() -> a shallow copy of T """
        return RBTree(self) # has no problem with sorted keys
    __copy__ = copy

    def _new_node(self, key, value):
        """ Create a new treenode """
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """ T.insert(key, value) <==> T[key] = value, insert key, value into Tree """
        compare = self.compare
        if self.root is None: # Empty tree case
            self.root = self._new_node(key, value)
            self.root.red = False # make root black
            return

        head = Node() # False tree root
        grand_parent = None
        grand_grand_parent = head
        parent = None # parent
        direction = 0
        last = 0

        # Set up helpers
        grand_grand_parent.right = self.root
        node = grand_grand_parent.right
        # Search down the tree
        while True:
            if node is None: # Insert new node at the bottom
                node = self._new_node(key, value)
                parent[direction] = node
            elif is_red(node.left) and is_red(node.right):# Color flip
                node.red = True
                node.left.red = False
                node.right.red = False

            # Fix red violation
            if is_red(node) and is_red(parent):
                direction2 = 1 if grand_grand_parent.right is grand_parent else 0
                if node is parent[last]:
                    grand_grand_parent[direction2] = jsw_single(grand_parent, 1-last)
                else:
                    grand_grand_parent[direction2] = jsw_double(grand_parent, 1-last)

            # Stop if found
            cmp_res = compare(key, node.key)
            if cmp_res == 0:
                node.value = value #set new value for key
                break

            last = direction
            direction = 0 if cmp_res < 0 else 1
            # Update helpers
            if grand_parent is not None:
                grand_grand_parent = grand_parent
            grand_parent = parent
            parent = node
            node = node[direction]

        self.root = head.right # Update root
        self.root.red = False # make root black

    def remove(self, key):
        """ T.remove(key) <==> del T[key], remove item <key> from tree """
        if self.root is None:
            raise KeyError(str(key))
        compare = self.compare
        head = Node() # False tree root
        node = head
        node.right = self.root
        parent = None
        grand_parent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while node[direction] is not None:
            last = direction

            # Update helpers
            grand_parent = parent
            parent = node
            node = node[direction]
            cmp_res = compare(key, node.key)
            direction = 1 if cmp_res > 0 else 0

            # Save found node
            if cmp_res == 0:
                found = node

            # Push the red node down
            if not is_red(node) and not is_red(node[direction]):
                if is_red(node[1-direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                elif not is_red(node[1-direction]):
                    sibling = parent[1-last]
                    if sibling is not None:
                        if (not is_red(sibling[1-last])) and (not is_red(sibling[last])):
                            # Color flip
                            parent.red = False
                            sibling.red = True
                            node.red = True
                        else:
                            direction2 = 1 if grand_parent.right is parent else 0
                            if is_red(sibling[last]):
                                grand_parent[direction2] = jsw_double(parent, last)
                            elif is_red(sibling[1-last]):
                                grand_parent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            grand_parent[direction2].red = True
                            node.red = True
                            grand_parent[direction2].left.red = False
                            grand_parent[direction2].right.red = False

        # Replace and remove if found
        if found is not None:
            found.key = node.key
            found.value = node.value
            parent[int(parent.right is node)] = node[int(node.left is None)]
            node.free()
            self._count -= 1

        # Update root and make it black
        self.root = head.right
        if self.root is not None:
            self.root.red = False
