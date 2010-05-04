#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010

import sys
import unittest2 as unittest
from itertools import izip

from random import randint, shuffle

set3 = [34, 67, 89, 123, 3, 7, 9, 2, 0, 999]

class CheckTree(object):
    default_values1 = zip([12, 34, 45, 16, 35, 57], [12, 34, 45, 16, 35, 57])
    default_values2 = [(2, 12), (4, 34), (8, 45), (1, 16), (9, 35), (3, 57)]

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
        del tree[50]
        self.assertTrue(tree.is_empty)

    def check_integrity(self, keys, remove_key, tree):
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
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_2(self):
        keys = [50, 25, 12]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_3(self):
        keys = [50, 25, 12, 33]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_4(self):
        keys = [50, 25, 12, 33, 40]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_5(self):
        keys = [50, 25, 12, 33, 40, 37, 43]
        tree = self.TREE.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_child_6(self):
        keys = [50, 75, 100, 150, 60, 65, 64, 80, 66]
        tree = self.TREE.fromkeys(keys)
        remove_key = 75
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_2(self):
        keys = [50, 25, 12, 33, 34]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_3(self):
        keys = [50, 25, 12, 33, 34, 75]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_4(self):
        keys = [50, 25, 12, 33, 34, 75, 60]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_remove_root_5(self):
        keys = [50, 25, 12, 33, 34, 75, 60, 61]
        tree = self.TREE.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(self.check_integrity(keys, remove_key, tree))

    def test_discard(self):
        keys = [50, 25, 12, 33, 34, 75, 60, 61]
        tree = self.TREE.fromkeys(keys)
        try:
            tree.discard(17)
        except KeyError:
            self.assertTrue(False, "Discard raises KeyError")

    def test_remove_shuffeld(self):
        keys = [50, 25, 20, 35, 22, 23, 27, 75, 65, 90, 60, 70, 85, 57, 83, 58]
        remove_keys = keys[:]
        for _ in range(10):
            shuffle(remove_keys)
            for remove_key in remove_keys:
                tree = self.TREE.fromkeys(keys)
                del tree[remove_key]
                for search_key in keys:
                    if search_key == remove_key:
                        self.assertFalse(search_key in tree)
                    else:
                        self.assertTrue(search_key in tree)

    def test_remove_random_numbers(self):
        try:
            with open('xtestkey.txt') as fp: # if you need known keys
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
        self.assertEqual(len(tree), 0)
        try:
            self.assertEqual(tree.root, None)
        except AttributeError:
            pass # no access to root for cython trees

    def test_setdefault(self):
        tree = self.TREE(self.default_values2)
        value = tree.setdefault(2, 17) # key <2> exists and == 12
        self.assertEqual(value, 12)
        value = tree.setdefault(99, 77)
        self.assertEqual(value, 77)

    def test_min_item(self):
        tree = self.TREE(zip(set3, set3))
        min_item = tree.min_item()
        self.assertEqual(min_item[1], 0)

    def test_max_item(self):
        tree = self.TREE(zip(set3, set3))
        max_item = tree.max_item()
        self.assertEqual(max_item[1], 999)

    def test_min_key(self):
        tree = self.TREE(zip(set3, set3))
        minkey = tree.min_key()
        self.assertEqual(minkey, 0)
        self.assertEqual(minkey, min(tree))

    def test_max_key(self):
        tree = self.TREE(zip(set3, set3))
        maxkey = tree.max_key()
        self.assertEqual(maxkey, 999)
        self.assertEqual(maxkey, max(tree))

    def test_prev_item(self):
        tree = self.TREE(zip(set3, set3))
        prev_value = None
        for key in tree.iterkeys():
            try:
                prev_item = tree.prev_item(key)
            except KeyError: # only on first key
                self.assertEqual(prev_value, None)
            if prev_value is not None:
                self.assertEqual(prev_value, prev_item[1])
            prev_value = key

    def test_succ_item(self):
        tree = self.TREE(zip(set3, set3))
        succ_value = None
        for key in reversed(tree.keys()):
            try:
                succ_item = tree.succ_item(key)
            except KeyError: # only on last key
                self.assertEqual(succ_value, None)
            if succ_value is not None:
                self.assertEqual(succ_value, succ_item[1])
            succ_value = key

    def test_prev_key(self):
        tree = self.TREE(zip(set3, set3))
        pkey = None
        for key in tree.iterkeys():
            try:
                prev_key = tree.prev_key(key)
            except KeyError: # only on first key
                self.assertEqual(pkey, None)
            if pkey is not None:
                self.assertEqual(pkey, prev_key)
            pkey = key

    def test_succ_key(self):
        tree = self.TREE(zip(set3, set3))
        skey = None
        for key in reversed(tree.keys()):
            try:
                succ_key = tree.succ_key(key)
            except KeyError: # only on last key
                self.assertEqual(skey, None)
            if skey is not None:
                self.assertEqual(skey, succ_key)
            skey = key

    def test_succ_prev_key_random_1000(self):
        keys = list(set([randint(0, 10000) for _ in xrange(1000)]))
        shuffle(keys)
        tree = self.TREE.fromkeys(keys)

        skey = None
        for key in reversed(tree.keys()):
            try:
                succ_key = tree.succ_key(key)
            except KeyError: # only on last key
                self.assertEqual(skey, None)
            if skey is not None:
                self.assertEqual(skey, succ_key)
            skey = key

        pkey = None
        for key in tree.iterkeys():
            try:
                prev_key = tree.prev_key(key)
            except KeyError: # only on first key
                self.assertEqual(pkey, None)
            if pkey is not None:
                self.assertEqual(pkey, prev_key)
            pkey = key

    def test_pop_min(self):
        tree = self.TREE(zip(set3, set3))
        keys = sorted(set3[:])
        for key in keys:
            k, v = tree.pop_min()
            self.assertEqual(key, v)

    def test_pop_max(self):
        tree = self.TREE(zip(set3, set3))
        keys = sorted(set3[:], reverse=True)
        for key in keys:
            k, v = tree.pop_max()
            self.assertEqual(key, v)

    def test_nlargest(self):
        l = range(30)
        shuffle(l)
        tree = self.TREE(zip(l, l))
        result = tree.nlargest(10)
        chk = [(x,x) for x in range(29, 19, -1)]
        self.assertEqual(chk, result)

    def test_nsmallest(self):
        l = range(30)
        shuffle(l)
        tree = self.TREE(zip(l, l))
        result = tree.nsmallest(10)
        chk = [(x,x) for x in range(0, 10)]
        self.assertEqual(chk, result)

    def test_reverse_iterkeys(self):
        tree = self.TREE(zip(set3, set3))
        result = reversed(sorted(set3))
        for key in tree.iterkeys(reverse=True):
            chk = next(result)
            self.assertEqual(chk, key)

    def test_reversed(self):
        tree = self.TREE(zip(set3, set3))
        result = reversed(sorted(set3))
        for key, chk in izip(reversed(tree), result):
            self.assertEqual(chk, key)

    def test_item_at(self):
        tree = self.TREE(self.default_values2)
        expected = [1, 2, 3, 4, 8, 9]
        for index in range(len(tree)):
            self.assertEqual(expected[index], tree.item_at(index)[0])

    def test_index(self):
        tree = self.TREE(self.default_values2)
        expected = [1, 2, 3, 4, 8, 9]
        self.assertEqual(tree.index(1), 0)
        self.assertEqual(tree.index(2), 1)
        self.assertEqual(tree.index(8), 4)
        self.assertEqual(tree.index(9), 5)

    def test_slice(self):
        tree = self.TREE(self.default_values2)
        expected = [1, 2, 3, 4, 8, 9]
        result = tree[0:1]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)

        result = tree[1: 3] # 2, 3
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1][0], 3)

        result = tree[3:]# 4, 8, 9
        self.assertEqual(len(result), 3)
        self.assertEqual(result[2][0], 9)

        result = tree[:3] #  1, 2, 3
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 1)

        result = tree[5:2:-1] # 9, 8, 4
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 9)

        result = tree[::2] # 1, 3, 8
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[1][0], 3)
        self.assertEqual(result[2][0], 8)

        result = tree[6::-2] # 9, 4, 2
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 9)
        self.assertEqual(result[1][0], 4)
        self.assertEqual(result[2][0], 2)

    def test_nlargest_by_slicing(self):
        l = range(30)
        shuffle(l)
        tree = self.TREE(zip(l, l))
        result1 = tree.nlargest(10)
        result2 = list(reversed(tree[-10:]))
        self.assertEqual(result1, result2)

    def test_nsmallest_by_slicing(self):
        l = range(30)
        shuffle(l)
        tree = self.TREE(zip(l, l))
        result1 = tree.nsmallest(10)
        result2 = tree[0:10]
        self.assertEqual(result1, result2)

    def test_intersection(self):
        l1 = range(30)
        shuffle(l1)
        l2 = range(15, 45)
        shuffle(l2)

        tree1 = self.TREE(zip(l1, l1))
        tree2 = self.TREE(zip(l2, l2))
        i = tree1 & tree2
        self.assertEqual(len(i), 15)
        self.assertEqual(i.min_key(), 15)
        self.assertEqual(i.max_key(), 29)

    def test_union(self):
        l1 = range(30)
        shuffle(l1)
        l2 = range(15, 45)
        shuffle(l2)

        tree1 = self.TREE(zip(l1, l1))
        tree2 = self.TREE(zip(l2, l2))
        i = tree1 | tree2
        self.assertEqual(len(i), 45)
        self.assertEqual(i.min_key(), 0)
        self.assertEqual(i.max_key(), 44)

    def test_difference(self):
        l1 = range(30)
        shuffle(l1)
        l2 = range(15, 45)
        shuffle(l2)

        tree1 = self.TREE(zip(l1, l1))
        tree2 = self.TREE(zip(l2, l2))
        i = tree1 - tree2
        self.assertEqual(len(i), 15)
        self.assertEqual(i.min_key(), 0)
        self.assertEqual(i.max_key(), 14)

    def test_symmetric_difference(self):
        l1 = range(30)
        shuffle(l1)
        l2 = range(15, 45)
        shuffle(l2)

        tree1 = self.TREE(zip(l1, l1))
        tree2 = self.TREE(zip(l2, l2))
        i = tree1 ^ tree2
        self.assertEqual(len(i), 30)
        self.assertEqual(i.min_key(), 0)
        self.assertEqual(i.max_key(), 44)
        self.assertTrue(15 not in i)
        self.assertTrue(29 not in i)

if __name__=='__main__':
    unittest.main()
