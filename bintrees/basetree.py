#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: abstract tree module
# Created: 28.04.2010

from itertools import izip

class BaseTree(object):
    def __init__(self, items=[], compare=None):
        self.root = None
        self.compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    def __repr__(self):
        def _tostr(node):
            if (node is not None) and (not node.is_nil):
                result = []
                left = _tostr(node.left)
                right = _tostr(node.right)
                nodestr = repr(node.key)+': '+repr(node.value)
                if left is not None:
                    result.extend(left)
                result.append(nodestr)
                if right is not None:
                    result.extend(right)
                return result
            else:
                return None
        return "{{{0}}}".format(", ".join(_tostr(self.root)))

    def has_key(self, key):
        node = self._find_node(self.root, key)
        return node is not None
    __contains__ = has_key

    def clear(self):
        def _clear(node):
            if node is not None:
                _clear(node.left)
                _clear(node.right)
                node.free()
        _clear(self.root)
        self.root = None

    def __len__(self):
        if self._count == 0:
            self.count()
        return self._count

    def count(self):
        def _count(node):
            self._count += 1
        self._count = 0
        if self.root is not None:
            self.foreach(_count)

    def is_empty(self):
        return self.root is None

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        def _iterkeys(node):
            if node is not None:
                for key in _iterkeys(node.left):
                    yield key
                yield node.key
                for key in _iterkeys(node.right):
                    yield key
        return _iterkeys(self.root)
    __iter__ = iterkeys

    def values(self):
        return list(self.itervalues())

    def itervalues(self):
        def _itervalues(node):
            if node is not None:
                for value in _itervalues(node.left):
                    yield value
                yield node.value
                for value in _itervalues(node.right):
                    yield value
        return _itervalues(self.root)

    def iteritems(self):
        return izip(self.iterkeys(), self.itervalues())

    def items(self):
        return list(self.iteritems())

    def __getitem__(self, key):
        node = self._find_node(self.root, key)
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
        if isinstance(other, _Tree):
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
        node = self._find_node(self.root, key)
        if node is None:
            self.insert(default)
            return default
        return node.data

    def foreach(self, func, order='inorder'):
        """Visit all tree nodes and process node-value.

        func -- function(node.value)

        order -- 'inorder', 'preorder', 'postorder'
        """
        def _traverse_inorder(node):
            if node is None: return
            _traverse_inorder(node.left)
            func(node.value)
            _traverse_inorder(node.right)

        def _traverse_preorder(node):
            if node is None: return
            func(node.value)
            _traverse_preorder(node.left)
            _traverse_preorder(node.right)

        def _traverse_postorder(node):
            if node is None: return
            _traverse_postorder(node.left)
            _traverse_postorder(node.right)
            func(node.value)

        if order=='inorder':
            _traverse_inorder(self.root)
        elif order=='postorder':
            _traverse_postorder(self.root)
        elif order=='preorder':
            _traverse_preorder(self.root)
        else:
            raise ValueError("foreach(): unknown order '{0}'.".format(order))

    def _find_node(self, node, key):
        """Find node by <key>, returns <None> if not found.

        node -- start node (in most cases == self.root)
        """
        compare = self.compare
        while True:
            if node is None:
                return None
            cval = compare(key, node.key)
            if cval == 0:
                return node
            elif cval < 0:
                node = node.left
            else:
                node = node.right

    def _replace(self, oldnode, newnode):
        self._count -= 1
        parent = oldnode.parent
        if parent is None: #root
            self.root = newnode
        else:
            if parent.left is oldnode:
                parent.left = newnode
            else:
                parent.right = newnode

        if newnode is not None:
            if newnode is newnode.parent.left: # unlink newnode from old parent
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

    @staticmethod
    def _smallest_node(node):
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _biggest_node(node):
        while node.right is not None:
            node = node.right
        return node

    @classmethod
    def fromkeys(cls, iterable, value=None):
        tree = cls()
        for key in iterable:
            tree.insert(key, value)
        return tree

    def get(self, key, default=None):
        node = self._find_node(self.root, key)
        if node is None:
            return default
        else:
            return node.value

    def pop(self, key, *args):
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got {0}".format(
                              1+len(args)))
        node = self._find_node(self.root, key)
        if node is None:
            if len(args) == 0:
                raise KeyError(unicode(key))
            else:
                return args[0]
        value = node.value
        self.remove(key)
        return value

    def popitem(self):
        if self.is_empty():
            raise KeyError("popitem(): tree is empty")
        node = self._get_leaf()
        result = (node.key, node.value)
        self.remove(node.key)
        return result

    def _get_leaf(self):
        node = self.root
        while True:
            if node.left is not None:
                node = node.left
            elif node.right is not None:
                node = node.right
            else:
                return node

    def insert(self, data, key):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError
