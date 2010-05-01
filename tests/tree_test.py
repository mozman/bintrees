#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010

import sys
import unittest2 as unittest
from random import randint, shuffle

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
    draw_node(tree.root, (100, 100), 60)
    return dwg

class TestAbstTree(unittest.TestCase):
    default_values1 = zip([12, 34, 45, 16, 35, 57], [12, 34, 45, 16, 35, 57])
    default_values2 = [(2, 12), (4, 34), (8, 45), (1, 16), (9, 35), (3, 57)]
    @property
    def TREE(self):
        return dict

    def test_create_tree(self):
        tree = self.TREE()
        self.assertEqual(len(tree), 0)
        tree.update(self.default_values1)
        self.assertEqual(len(tree), 6)

    def test_iter_tree(self):

        tree = self.TREE(self.default_values1)
        result = list(iter(tree))
        self.assertEqual(result, [12, 16, 34, 35, 45, 57])

    def test_get_items(self):
        tree = self.TREE(self.default_values1)
        self.assertEqual(tree.get(34), 34)
        self.assertEqual(tree.get(12), 12)

    def test_remove_root_1(self):
        keys = [50,]
        tree = self.TREE.fromkeys(keys)
        tree.remove(50)
        self.assertTrue(tree.is_empty)

    def check_integrity(self, keys, remove_key, tree):
        try:
            if not tree._check_parent_links():
                return False
        except AttributeError:
            pass
        for search_key in keys:
            if search_key == remove_key:
                if search_key in tree:
                    return False
            else:
                if search_key not in tree:
                    return False
        return True

    def test_remove_child_1(self):
        keys = [50, 25]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_2(self):
        keys = [50, 25, 12]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_3(self):
        keys = [50, 25, 12, 33]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_4(self):
        keys = [50, 25, 12, 33, 40]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_5(self):
        keys = [50, 25, 12, 33, 40, 37, 43]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_6(self):
        keys = [50, 75, 100, 150, 60, 65, 64, 80, 66]
        tree = self.TREE.fromkeys(keys)
        remove_key = 75
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_2(self):
        keys = [50, 25, 12, 33, 34]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_3(self):
        keys = [50, 25, 12, 33, 34, 75]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_4(self):
        keys = [50, 25, 12, 33, 34, 75, 60]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_5(self):
        keys = [50, 25, 12, 33, 34, 75, 60, 61]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        tree.remove(remove_key)
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_shuffeld(self):
        keys = [50, 25, 20, 35, 22, 23, 27, 75, 65, 90, 60, 70, 85, 57, 83, 58]
        remove_keys = keys[:]
        for _ in range(10):
            shuffle(remove_keys)
            for remove_key in remove_keys:
                tree = self.TREE.fromkeys(keys)
                tree.remove(remove_key)
                for search_key in keys:
                    if search_key == remove_key:
                        self.assertFalse(search_key in tree)
                    else:
                        self.assertTrue(search_key in tree)

    def test_remove_random_numbers(self):
        try:
            with open('xtestkey.txt') as fp:
                keys = eval(fp.read())
        except IOError:
            keys = list(set([randint(0, 10000) for _ in xrange(1000)]))
        shuffle(keys)
        tree = self.TREE.fromkeys(keys)
        self.assertEqual(len(tree), len(keys))
        for key in keys:
            del tree[key]
        self.assertEqual(len(tree), 0)

    def test_order(self):
        keys = set([randint(0, 10000) for _ in xrange(1000)])
        tree = self.TREE.fromkeys(keys)
        generator = iter(tree)
        a = generator.next()
        for b in generator:
            self.assertGreaterEqual(b, a)
            a = b

    def test_index_operator(self):
        tree = self.TREE(self.default_values1)
        self.assertEqual(tree[45], 45)
        tree[99] = 99

    def test_complex_data(self):
        tree = self.TREE(self.default_values2)
        self.assertEqual(tree[8], 45)

    def test_default_vaule(self):
        tree = self.TREE(self.default_values2)
        self.assertEqual(tree.get(7, "DEFAULT"), "DEFAULT")

    def test_has_key(self):
        tree = self.TREE(self.default_values2)
        self.assertTrue(tree.has_key(8))
        self.assertFalse(tree.has_key(11))
        self.assertTrue( 8 in tree)
        self.assertFalse(8 not in tree)
        self.assertFalse(11 in tree)
        self.assertTrue(11 not in tree)

    def test_pop(self):
        tree = self.TREE(self.default_values2)
        data = tree.pop(8)
        self.assertEqual(data, 45)
        self.assertFalse(8 in tree)
        self.assertRaises(KeyError, tree.pop, 8)
        self.assertEqual(tree.pop(8, 99), 99)

    def test_popitem(self):
        tree = self.TREE(self.default_values2)
        d = dict()
        while not tree.is_empty():
            key, value = tree.popitem()
            d[key]=value
        expected = {2: 12, 4: 34, 8: 45, 1: 16, 9: 35, 3: 57}
        self.assertEqual(expected, d)
        self.assertRaises(KeyError, tree.popitem)

    def test_iterkeys(self):
        tree = self.TREE(self.default_values2)
        keys = tree.keys()
        expected = [1, 2, 3, 4, 8, 9]
        self.assertEqual(expected, keys)

    def test_itervalues(self):
        tree = self.TREE(self.default_values2)
        values = tree.values()
        expected = [16, 12, 57, 34, 45, 35]
        self.assertEqual(expected, values)

    def test_copy(self):
        tree = self.TREE(self.default_values2)
        copytree = tree.copy()
        self.assertEqual(tree.items(), copytree.items())

    def test_to_dict(self):
        tree = self.TREE(self.default_values2)
        d = dict(tree)
        self.assertEqual(d, dict(self.default_values2))

    def test_clear(self):
        tree = self.TREE(self.default_values2)
        tree.clear()
        self.assertEqual(tree.root, None)

    def test_setdefault(self):
        tree = self.TREE(self.default_values2)
        value = tree.setdefault(2, 17) # key <2> exists and == 12
        self.assertEqual(value, 12)
        value = tree.setdefault(99, 77)
        self.assertEqual(value, 77)

if __name__=='__main__':
    unittest.main()