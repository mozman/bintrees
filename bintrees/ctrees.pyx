#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython abstract tree module
# Created: 28.04.2010

from itertools import izip
from random import shuffle

__all__ = ['cBinaryTree', 'cRBTree', 'cAVLTree']

cdef class Node:
    cdef Node parent
    cdef Node left
    cdef Node right
    cdef object key
    cdef object value

    def __init__(self, object key, object value, Node parent):
        self.parent = parent
        self.left = None
        self.right = None
        self.key = key
        self.value = value

    cdef void free(self):
        self.left = None
        self.right = None
        self.parent = None
        self.key = None
        self.value = None

    cdef Node grandparent(self):
        if self.parent is not None:
            return self.parent.parent
        else:
            return None

    cdef Node uncle(self):
        cdef Node gparent
        cdef Node uncle

        gparent = self.grandparent()
        if gparent is None:
            return None

        uncle = gparent.left
        if self.parent is uncle:
            uncle = gparent.right
        return uncle

    cdef bint is_leftnode(self):
        return self is self.parent.left

    cdef bint is_rightnode(self):
        return self is self.parent.right

    cdef Node sibling(self):
        cdef Node _sibiling
        _sibiling = self.parent.left
        if self == _sibiling:
            _sibiling = self.parent.right
        return _sibiling

cdef object tree_to_str(Node node):
    if node is None:
        result = []
        left = tree_to_str(node.left)
        right = tree_to_str(node.right)
        nodestr = repr(node.key)+': '+repr(node.value)
        if left is not None:
            result.extend(left)
        result.append(nodestr)
        if right is not None:
            result.extend(right)
        return result
    else:
        return None

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

cdef Node smallest_node(Node node):
    while node.left is not None:
        node = node.left
    return node

cdef Node biggest_node(Node node):
    while node.right is not None:
        node = node.right
    return node

cdef Node get_leaf(Node node):
    while True:
        if node.left is not None:
            node = node.left
        elif node.right is not None:
            node = node.right
        else:
            return node

cdef class cBaseTree:
    cdef Node root
    cdef object compare
    cdef int _count

    def __init__(self, items=[], compare=None):
        self.root = None
        self.compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    def __repr__(self):
        treestrings = tree_to_str(self.root)
        return "{{{0}}}".format(", ".join(treestrings))

    def has_key(self, key):
        cdef Node node
        node = self.find_node(key)
        return node is not None
    __contains__ = has_key

    def clear(self):
        clear_tree(self.root)
        self.root = None

    def __len__(self):
        return self._count

    def is_empty(self):
        return (self.root is None)

    def keys(self):
        result = list()
        add_keys(self.root, result)
        return result

    def iterkeys(self):
        return iter(self.keys())
    __iter__ = iterkeys

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

    def __cmp__(self, other):
        if other is None:
            return 1
        if isinstance(other, cBaseTree):
            for key in self.iterkeys():
                value1 = self.__getitem__(key)
                try:
                    value2 = other.__getitem__(key)
                except KeyError:
                    # if <key> does not exists in <other>, <self> is greater
                    # than <other>
                    return 1
                cmp_res = cmp(value1, value2)
                if cmp_res != 0:
                    return cmp_res
            return 0
        else:
            raise ValueError('<self> is not comparable with <other>')

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

    cdef void replace(self, Node oldnode, Node newnode):
        cdef Node parent
        self._count -= 1
        parent = oldnode.parent
        if parent is None: #root
            self.root = newnode
        else:
            if parent.left == oldnode:
                parent.left = newnode
            else:
                parent.right = newnode

        if newnode is None:
            if newnode == newnode.parent.left: # unlink newnode from old parent
                newnode.parent.left = None
            else:
                newnode.parent.right = None
            newnode.parent = parent # link to newnode to new parent
            newnode.left = oldnode.left
            newnode.right = oldnode.right

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

cdef class cBinaryTree(cBaseTree):
    def copy(self):
        treekeys = self.keys()
        shuffle(treekeys)  # sorted keys generates a linked list!
        newtree = cBinaryTree()
        for key in treekeys:
            newtree[key] = self[key]
        return newtree
    __copy__ = copy

    def __len__(self):
        return self._count

    def new_node(self, key, value, parent):
        """Create a new tree node."""
        self._count += 1
        return Node(key, value, parent)

    def insert(self, key, value):
        if self.root is None:
            self.root = self.new_node(key, value, None)
        else:
            self._insert(self.root, key, value)

    cdef _insert(self, Node node, key, value):
        cdef int cval
        cval = self.compare(key, node.key)
        if cval == 0:
            node.value = value
        elif cval < 0:
            if node.left is None:
                node.left = self.new_node(key, value, node)
            else:
                self._insert(node.left, key, value)
        else:
            if node.right is None:
                node.right = self.new_node(key, value, node)
            else:
                self._insert(node.right, key, value)

    def remove(self, key):
        node = self.find_node(key)
        if node is None:
            raise KeyError(unicode(key))
        else:
            if node.left is None:
                child = node.right
            elif node.right is None:
                child = node.left
            else: #left and right != None
                child = smallest_node(node.right)
            self.replace(node, child)
        node.free()

cdef class RBNode(Node):
    cdef int color

    def __init__(self, object key, object value, Node parent, int color):
        Node.__init__(self, key, value, parent)
        self.color = color

DEF BLACK = 0
DEF RED = 1

cdef class cRBTree(cBaseTree):
    def copy(self):
        return cRBTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value, parent, color):
        self._count += 1
        return RBNode(key, value, parent, color)

    def insert(self, key, value):
        if (self.root is None):
            self.root = self.new_node(key, value, None, BLACK)
        else:
            self._insert(self.root, key, value)

    cdef _insert(self, RBNode node, key, value):
        cdef int cval
        cval = <int> self.compare(key, node.key)
        if cval == 0:
            node.value = value
        elif cval < 0:
            if node.left is None:
                node.left = self.new_node(key, value, node, RED)
                self.insert_case1(node.left)
            else:
                self._insert(node.left, key, value)
        else:
            if node.right is None:
                node.right = self.new_node(key, value, node, RED)
                self.insert_case1(node.right)
            else:
                self._insert(node.right, key, value)

    cdef rotate_right(self, RBNode w):
        cdef RBNode, root, s, u
        root = w.parent
        s = w.left
        u = s.right

        if root is not None:
            if w.is_leftnode():
                root.left = s
            else:
                root.right = s
        else:
            self.root = s

        s.right = w
        w.left = u
        if u is not None:
            u.parent = w
        w.parent = s
        s.parent = root

    cdef rotate_left(self, RBNode s):
        cdef RBNode root, w, u
        root = s.parent
        w = s.right
        u = w.left

        if root is not None:
            if s.is_leftnode():
                root.left = w
            else:
                root.right = w
        else:
            self.root = w

        s.right = u
        w.left = s
        if u is not None:
            u.parent = s
        s.parent = w
        w.parent = root

    def remove(self, key):
        cdef RBNode node, child
        node = self.find_node(key)
        if node is None:
            raise KeyError(unicode(key))
        else:
            if node.left is None:
                child = node.right
            elif node.right is None:
                child = node.left
            else: #left and right not nil
                child = smallest_node(node.right)
            self.replace(node, child)
            if (node.color == BLACK) and (child is not None):
                if child.color == RED:
                    child.color == BLACK
                else:
                    self.delete_case1(child)
        node.free()

    cdef void insert_case1(self, RBNode node):
        if node.parent is None:
            node.color = BLACK
        elif node.parent.color == RED:
            self.insert_case3(node)

    cdef void insert_case3(self, RBNode node):
        cdef RBNode uncle, gparent
        uncle = node.uncle()
        if (uncle is not None) and (uncle.color == RED):
            gparent = node.grandparent()
            node.parent.color = BLACK
            uncle.color = BLACK
            gparent.color = RED
            self.insert_case1(gparent)
        else:
            self.insert_case4(node)

    cdef void insert_case4(self, RBNode node):
        if node.is_rightnode() and node.parent.is_leftnode():
            self.rotate_left(node.parent)
            node = node.left
        elif node.is_leftnode() and node.parent.is_rightnode():
            self.rotate_right(node.parent)
            node = node.right
        self.insert_case5(node)

    cdef void insert_case5(self, RBNode node):
        cdef RBNode gparent
        gparent = node.parent.grandparent()
        node.parent.color = BLACK
        gparent.color = RED
        if node.is_leftnode() and node.parent.is_leftnode():
            self.rotate_right(gparent)
        else:
            self.rotate_left(gparent)

    cdef void delete_case1(self, RBNode node):
        if (node.parent is not None):
            self.delete_case2(node)

    cdef void delete_case2(self, RBNode node):
        cdef RBNode sibling
        sibling = node.sibling()
        if (sibling.color == RED):
            node.parent.color = RED
            sibling.color = BLACK
            if node.is_leftnode():
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
        self.delete_case3(node)

    cdef void delete_case3(self, RBNode node):
        cdef RBNode sibling
        sibling = node.sibling()
        if (node.parent.color == BLACK) and \
           (sibling.color == BLACK) and \
           (sibling.left.color == BLACK) and \
           (sibling.right.color == BLACK):
            sibling.color = RED
            self.delete_case1(node.parent)
        else:
            self.delete_case4(node)

    cdef void delete_case4(self, RBNode node):
        cdef RBNode sibling
        sibling = node.sibling()
        if (node.parent.color == RED) and \
           (sibling.color == BLACK) and \
           (sibling.left.color == BLACK) and \
           (sibling.right.color == BLACK):
            sibling.color = RED
            node.parent.color = BLACK
        else:
            self.delete_case5(node)

    cdef void delete_case5(self, RBNode node):
        cdef RBNode sibling
        sibling = node.sibling()
        if node.is_leftnode() and \
           (sibling.color == BLACK) and \
           (sibling.left.color == RED) and \
           (sibling.right.color == BLACK):

            sibling.color = RED
            sibling.left.color = BLACK
            self.rotate_right(sibling)
        elif node.is_rightnode() and \
          (sibling.color == BLACK) and \
          (sibling.right.color == RED) and \
          (sibling.left.color == BLACK):
            sibling.color = RED
            sibling.right.color = BLACK
            self.rotate_left(sibling)
        self.delete_case6(node)

    cdef void delete_case6(self, RBNode node):
        cdef RBNode sibling
        sibling = node.sibling()
        sibling.color = node.parent.color
        node.parent.color = BLACK
        if node.is_leftnode():
            sibling.right.color = BLACK
            self.rotate_left(node.parent)
        else:
            sibling.left.color = BLACK
            self.rotate_right(node.parent)

DEF LEFT = 0
DEF RIGHT = 1

cdef class AVLNode(Node):
    cdef int height

    def __init__(self, key=None, value=None, parent=None):
        Node.__init__(self, key, value, parent)
        self.height = 1

    cdef AVLNode get_child(self, int side):
        if side == LEFT:
            return self.left
        else:
            return self.right

    cdef void set_child(self, int side, AVLNode node):
        if side == LEFT:
            self.left = node
        else:
            self.right = node

    cdef void update_height(self):
        cdef int left_height
        cdef int right_height
        left_height = subtree_height(self.left)
        right_height = subtree_height(self.right)

        if left_height > right_height:
            self.height = left_height + 1
        else:
            self.height = right_height + 1

    cdef int node_parent_side(self):
        if self.parent.left is self:
            return LEFT
        else:
            return RIGHT

cdef int subtree_height(AVLNode node):
    if node is None:
        return 0
    else:
        return node.height

cdef class cAVLTree(cBaseTree):
    def copy(self):
        return cAVLTree(self)
    __copy__ = copy

    cdef void node_replace(self, AVLNode node1, AVLNode node2):
        cdef int side
        if node2 is not None:
            node2.parent = node1.parent
        if node1.parent is None:
            self.root = node2
        else:
            side = node1.node_parent_side()
            node1.parent.set_child(side, node2)
            node1.parent.update_height()

    cdef AVLNode rotate(self, AVLNode node, int direction):
        cdef AVLNode new_root
        cdef int other_side
        other_side = 1 - direction

        new_root = node.get_child(other_side)
        self.node_replace(node, new_root)
        node.set_child(other_side, new_root.get_child(direction))
        new_root.set_child(direction, node)
        node.parent = new_root

        if node.get_child(other_side) is not None:
            node.get_child(other_side).parent = node

        new_root.update_height()
        node.update_height()
        return new_root


    cdef AVLNode node_balance(self, AVLNode node):
        cdef AVLNode left_subtree, right_subtree
        cdef AVLNode child
        cdef int diff
        left_subtree = node.left
        right_subtree = node.right

        diff = subtree_height(right_subtree) - subtree_height(left_subtree)
        if (diff >= 2):
            child = right_subtree

            if subtree_height(child.right) < subtree_height(child.left):
                self.rotate(right_subtree, RIGHT)
                node = self.rotate(node, LEFT);
        elif (diff <= -2):
            child = node.left
            if subtree_height(child.left) < subtree_height(child.right):
                self.rotate(left_subtree, LEFT)
            node = self.rotate(node, RIGHT);
        node.update_height()
        return node

    cdef balance_to_root(self, AVLNode root):
        cdef AVLNode rover

        rover = root
        while rover is not None:
            root = self.node_balance(rover)
            rover = root.parent
        self.root = root

    def insert(self, key, value):
        cdef AVLNode rover
        cdef AVLNode previous_node
        cdef AVLNode new_node
        cdef int cmp_res, ipos

        rover = self.root
        previous_node = None
        compare = self.compare

        while rover is not None:
            previous_node = rover
            cmp_res = compare(key, rover.key)
            if cmp_res < 0:
                rover = rover.left
                ipos = LEFT
            elif cmp_res > 0:
                rover = rover.right
                ipos = RIGHT
            else:
                rover.value = value
                return

        new_node = AVLNode(key, value, previous_node)
        self._count += 1

        if previous_node is not None:
            previous_node.set_child(ipos, new_node)

        self.balance_to_root(previous_node)

        if self.root is None:
            self.root = new_node

    cdef AVLNode get_replacement(self, node):
        cdef AVLNode left_subtree
        cdef AVLNode right_subtree
        cdef AVLNode child
        cdef int left_height, right_height, other_side

        left_subtree = node.left
        right_subtree = node.right

        if (left_subtree is None) and (right_subtree is None):
            return None

        left_height = subtree_height(left_subtree)
        right_height = subtree_height(right_subtree)

        if (left_height < right_height):
            side = RIGHT
        else:
            side = LEFT

        result = node.get_child(side)
        other_side = 1 - side
        while (result.get_child(other_side) is not None):
            result = result.get_side(other_side)

        child = result.get_child(side)
        self.node_replace(result, child)

        result.parent.update_height()
        return result

    cdef void remove_node(self, AVLNode node):
        cdef AVLNode swap_node
        cdef AVLNode balance_startpoint
        cdef AVLNode child
        cdef int i

        swap_node = self.get_replacement(node)
        if swap_node is None:
            self.node_replace(node, None)
            balance_startpoint = node.parent
        else:
            if swap_node.parent is None:
                balance_startpoint = swap_node
            else:
                balance_startpoint = swap_node.parent
            for i in range(2):
                child = node.get_child(i)
                swap_node.set_child(i, child)
                if child is not None:
                    child.parent = swap_node
            swap_node.height = node.height
            self.node_replace(node, swap_node);

        self.balance_to_root(balance_startpoint)
        node.free()
        self._count -= 1

    def remove(self, key):
        cdef AVLNode node
        node = self.find_node(key)
        if node is None:
            raise KeyError(str(key))
        self.remove_node(node)
