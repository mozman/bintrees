#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010

import sys
import unittest2 as unittest
from random import randint, shuffle

from bintrees.rbtree import RBTree

import dxfwrite

def draw_tree(tree, fname, key=-1):
    def draw_node(node, pos, dx):
        dwg.add(dxf.text(str(node.key), halign=dxfwrite.CENTER, insert=pos, alignpoint=pos, height=0.1))
        if node.left is not None:
            pos2 = (pos[0]-dx, pos[1]+dy)
            dwg.add(dxf.line(pos, pos2))
            draw_node(node.left, pos2, dx*fact)
        if node.right is not None:
            pos3 = (pos[0]+dx, pos[1]+dy)
            dwg.add(dxf.line(pos, pos3))
            draw_node(node.right, pos3, dx*fact)
    dy = 1
    fact = 0.45
    dxf = dxfwrite.DXFEngine
    dwg = dxf.drawing(fname)
    if key != -1:
        dwg.add(dxf.text('before remove key: ' + str(key), insert=(100, 95)))
    draw_node(tree.root, (100, 100), 40)
    return dwg

class TestRBTree(unittest.TestCase):
    default_values1 = zip([12, 34, 45, 16, 35, 57], [12, 34, 45, 16, 35, 57])
    default_values2 = [(2, 12), (4, 34), (8, 45), (1, 16), (9, 35), (3, 57)]

    def test_create_tree(self):
        tree = RBTree()
        self.assertEqual(len(tree), 0)
        tree.update(self.default_values1)
        self.assertEqual(len(tree), 6)

    def test_iter_tree(self):
        tree = RBTree(self.default_values1)
        result = list(iter(tree))
        self.assertEqual(result, [12, 16, 34, 35, 45, 57])

    def test_get_items(self):
        tree = RBTree(self.default_values1)
        self.assertEqual(tree.get(34), 34)
        self.assertEqual(tree.get(12), 12)

    def test_remove(self):
        keys = [50, 25, 20, 35, 22, 23, 27, 75, 65, 90, 60, 70, 85, 57, 83, 58]
        data = dict.fromkeys(keys)
        for remove_key in keys:
            tree = RBTree.fromkeys(keys)
            tree.remove(remove_key)
            for search_key in keys:
                if search_key == remove_key:
                    self.assertFalse(search_key in tree)
                else:
                    self.assertTrue(search_key in tree)

    def test_remove_shuffled(self):
        keys = [50, 25, 20, 35, 22, 23, 27, 75, 65, 90, 60, 70, 85, 57, 83, 58]
        data = dict.fromkeys(keys)
        remove_keys = keys[:]
        for _ in range(10):
            shuffle(remove_keys)
            for remove_key in remove_keys:
                tree = RBTree.fromkeys(keys)
                tree.remove(remove_key)
                for search_key in keys:
                    if search_key == remove_key:
                        self.assertFalse(search_key in tree)
                    else:
                        self.assertTrue(search_key in tree)

    def test_delete_node(self):
        tree = RBTree(self.default_values1)
        del tree[57]
        self.assertFalse(57 in tree)

    def test_remove_random_numbers(self):
        keys = list(set([randint(0, 10000) for _ in xrange(1000)]))
        #with open('testkey.txt') as fp:
        #    keys = eval(fp.read())
        tree = RBTree.fromkeys(keys)
        #draw_tree(tree, 'rbtree.dxf').save()
        self.assertEqual(len(tree), len(keys))
        for key in keys:
            del tree[key]
        self.assertEqual(len(tree), 0)

    def test_order(self):
        keys = set([randint(0, 10000) for _ in xrange(1000)])
        tree = RBTree.fromkeys(keys)
        generator = iter(tree)
        a = generator.next()
        for b in generator:
            self.assertGreaterEqual(b, a)
            a = b

    def test_index_operator(self):
        tree = RBTree(self.default_values1)
        self.assertEqual(tree[45], 45)
        tree[99] = 99

    def test_complex_data(self):
        tree = RBTree(self.default_values2)
        self.assertEqual(tree[8], 45)

    def test_default_vaule(self):
        tree = RBTree()
        self.assertEqual(tree.get(7, "DEFAULT"), "DEFAULT")

    def test_has_key(self):
        tree = RBTree(self.default_values2)
        self.assertTrue(tree.has_key(8))
        self.assertFalse(tree.has_key(11))
        self.assertTrue( 8 in tree)
        self.assertFalse(8 not in tree)
        self.assertFalse(11 in tree)
        self.assertTrue(11 not in tree)

    def test_pop(self):
        tree = RBTree(self.default_values2)
        data = tree.pop(8)
        self.assertEqual(data, 45)
        self.assertFalse(8 in tree)
        self.assertRaises(KeyError, tree.pop, 8)
        self.assertEqual(tree.pop(8, 99), 99)

    def test_popitem(self):
        tree = RBTree(self.default_values2)
        d = dict()
        while not tree.is_empty():
            key, value = tree.popitem()
            d[key]=value
        expected = {2: 12, 4: 34, 8: 45, 1: 16, 9: 35, 3: 57}
        self.assertEqual(expected, d)
        self.assertRaises(KeyError, tree.popitem)

    def test_iterkeys(self):
        tree = RBTree(self.default_values2)
        keys = tree.keys()
        expected = [1, 2, 3, 4, 8, 9]
        self.assertEqual(expected, keys)

    def test_itervalues(self):
        tree = RBTree(self.default_values2)
        values = tree.values()
        expected = [16, 12, 57, 34, 45, 35]
        self.assertEqual(expected, values)

    def test_copy(self):
        tree = RBTree(self.default_values2)
        copytree = tree.copy()
        self.assertEqual(tree.items(), copytree.items())

    def test_clear(self):
        tree = RBTree(self.default_values2)
        tree.clear()
        self.assertEqual(tree.root, None)

    def test_to_dict(self):
        tree = RBTree(self.default_values2)
        d = dict(tree)
        self.assertEqual(d, dict(self.default_values2))

if __name__=='__main__':
    unittest.main()