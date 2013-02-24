#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

import sys
PYPY = hasattr(sys, 'pypy_version_info')

import unittest
import pickle

from random import randint, shuffle

from bintrees import BinaryTree, AVLTree, RBTree
from bintrees import FastBinaryTree, FastAVLTree, FastRBTree

set3 = [34, 67, 89, 123, 3, 7, 9, 2, 0, 999]


def check_integrity(keys, remove_key, tree):
    for search_key in keys:
        if search_key == remove_key:
            if search_key in tree:
                return False
        else:
            if search_key not in tree:
                return False
    return True


def randomkeys(num, maxnum=100000):
    keys = set([randint(0, maxnum) for _ in range(num)])
    while len(keys) != num:
        keys.add(randint(0, maxnum))
    return list(keys)


class CheckTree(object):
    default_values1 = list(zip([12, 34, 45, 16, 35, 57], [12, 34, 45, 16, 35, 57]))
    default_values2 = [(2, 12), (4, 34), (8, 45), (1, 16), (9, 35), (3, 57)]
    slicetest_data = [(1, 1), (2, 2), (3, 3), (4, 4), (8, 8), (9, 9), (10, 10), (11, 11)]

    def test_001_init(self):
        tree = self.TREE_CLASS()
        self.assertEqual(len(tree), 0)
        tree.update(self.default_values1)
        self.assertEqual(len(tree), 6)

    def test_002_init_with_dict(self):
        tree = self.TREE_CLASS(dict(self.default_values1))
        self.assertEqual(len(tree), 6)

    def test_000_init_with_seq(self):
        tree = self.TREE_CLASS(self.default_values1)
        self.assertEqual(len(tree), 6)

    def test_004_init_with_tree(self):
        tree1 = self.TREE_CLASS(self.default_values1)
        tree2 = self.TREE_CLASS(tree1)
        self.assertEqual(len(tree2), 6)

    def test_006_copy(self):
        tree1 = self.TREE_CLASS(self.default_values1)
        tree2 = tree1.copy()
        self.assertEqual(list(tree1.items()), list(tree2.items()))

    def test_007_to_dict(self):
        tree = self.TREE_CLASS(self.default_values2)
        d = dict(tree)
        self.assertEqual(d, dict(self.default_values2))

    def test_008a_repr(self):
        tree = self.TREE_CLASS(self.default_values2)
        clsname = tree.__class__.__name__
        reprstr = repr(tree)
        self.assertEqual(reprstr, '%s({1: 16, 2: 12, 3: 57, 4: 34, 8: 45, 9: 35})' % clsname)

    def test_008b_repr_empty_tree(self):
        tree = self.TREE_CLASS()
        self.assertEqual(repr(tree), tree.__class__.__name__ + '({})')

    def test_009_clear(self):
        tree = self.TREE_CLASS(self.default_values2)
        tree.clear()
        self.assertEqual(len(tree), 0)

    def test_010_contains(self):
        tree1 = self.TREE_CLASS(self.default_values2)
        tree2 = self.TREE_CLASS(self.default_values1)
        for key in tree1.keys():
            self.assertFalse(key in tree2)
        for key in tree2.keys():
            self.assertTrue(key in tree2)

    def test_011_is_empty(self):
        tree = self.TREE_CLASS()
        self.assertTrue(tree.is_empty())
        tree[0] = 1
        self.assertFalse(tree.is_empty())

    def test_012_update_1(self):
        tree = self.TREE_CLASS()
        tree.update({1: 'one', 2: 'two'})
        tree.update([(3, 'three'), (2, 'zwei')])
        self.assertEqual(list(tree.keys()), [1, 2, 3])
        self.assertEqual(list(tree.values()), ['one', 'zwei', 'three'])

    def test_013_update_2(self):
        tree = self.TREE_CLASS()
        tree.update({1: 'one', 2: 'two'}, [(3, 'three'), (2, 'zwei')])
        self.assertEqual(list(tree.keys()), [1, 2, 3])
        self.assertEqual(list(tree.values()), ['one', 'zwei', 'three'])

    def test_014_unique_keys(self):
        tree = self.TREE_CLASS()
        for value in range(5):
            tree[0] = value
        self.assertEqual(tree[0], 4)
        self.assertEqual(len(tree), 1)

    def test_015_getitem(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        for key in [12, 34, 45, 16, 35, 57]:
            self.assertEqual(key, tree[key])

    def test_016_setitem(self):
        tree = self.TREE_CLASS()
        for key in [12, 34, 45, 16, 35, 57]:
            tree[key] = key
        for key in [12, 34, 45, 16, 35, 57]:
            self.assertEqual(key, tree[key])

    def test_017_setdefault(self):
        tree = self.TREE_CLASS(self.default_values2)
        value = tree.setdefault(2, 17)  # key <2> exists and == 12
        self.assertEqual(value, 12)
        value = tree.setdefault(99, 77)
        self.assertEqual(value, 77)

    def test_018_keys(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(iter(tree))
        self.assertEqual(result, [12, 16, 34, 35, 45, 57])
        self.assertEqual(result, list(tree.keys()))

    def test_018a_keyslice(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.keyslice(15, 36))
        self.assertEqual(result, [16, 34, 35])

    def test_018b_keyslice(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.keyslice(15, 35))
        self.assertEqual(result, [16, 34])

    def test_018c_keyslice_reverse(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = reversed(list(tree.keyslice(15, 36)))
        self.assertEqual(list(result), [35, 34, 16])

    def test_018d_slice_from_start(self):
        # values: 1, 2, 3, 4, 8, 9, 10, 11
        tree = self.TREE_CLASS(self.slicetest_data)
        result = list(tree[:4])
        self.assertEqual(list(result), [1, 2, 3])

    def test_018e_slice_til_end(self):
        # values: 1, 2, 3, 4, 8, 9, 10, 11
        tree = self.TREE_CLASS(self.slicetest_data)
        result = list(tree[8:])
        self.assertEqual(list(result), [8, 9, 10, 11])

    def test_018f_slice_from_start_til_end(self):
        # values: 1, 2, 3, 4, 8, 9, 10, 11
        tree = self.TREE_CLASS(self.slicetest_data)
        result = list(tree[:])
        self.assertEqual(list(result), [1, 2, 3, 4, 8, 9, 10, 11])

    def __test_018g_slice_produces_values(self):
        tree = self.TREE_CLASS([(1, 100), (2, 200), (3, 300)])
        result = list(tree[:])
        self.assertEqual(list(result), [100, 200, 300])

    def test_018g_slice_produces_keys(self):
        tree = self.TREE_CLASS([(1, 100), (2, 200), (3, 300)])
        result = list(tree[:])
        self.assertEqual(list(result), [1, 2, 3])

    def test_019_values(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.values())
        self.assertEqual(result, [12, 16, 34, 35, 45, 57])
        self.assertEqual(result, list(tree.values()))

    def test_020_items(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.items())
        self.assertEqual(result, list(sorted(self.default_values1)))
        self.assertEqual(result, list(tree.items()))

    def test_021_keys_reverse(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.keys(reverse=True))
        self.assertEqual(result, list(reversed([12, 16, 34, 35, 45, 57])))
        self.assertEqual(result, list(tree.keys(reverse=True)))

    def test_022_values_reverse(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.values(reverse=True))
        self.assertEqual(result, list(reversed([12, 16, 34, 35, 45, 57])))
        self.assertEqual(result, list(tree.values(reverse=True)))

    def test_023_items_reverse(self):
        tree = self.TREE_CLASS(self.default_values1)
        result = list(tree.items(reverse=True))
        self.assertEqual(result, list(tree.items(reverse=True)))

    def test_024_get(self):
        tree = self.TREE_CLASS(self.default_values1)
        self.assertEqual(tree.get(34), 34)
        self.assertEqual(tree.get(99), None)

    def test_025_get_default(self):
        tree = self.TREE_CLASS(self.default_values1)
        self.assertEqual(tree.get(99, -10), -10)  # get default value
        self.assertEqual(tree.get(34, -10), 34)  # key exist
        self.assertEqual(tree.get(7, "DEFAULT"), "DEFAULT")

    def test_026_remove_child_1(self):
        keys = [50, 25]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_027_remove_child_2(self):
        keys = [50, 25, 12]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_028_remove_child_3(self):
        keys = [50, 25, 12, 33]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_029_remove_child_4(self):
        keys = [50, 25, 12, 33, 40]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_030_remove_child_5(self):
        keys = [50, 25, 12, 33, 40, 37, 43]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 25
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_031_remove_child_6(self):
        keys = [50, 75, 100, 150, 60, 65, 64, 80, 66]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 75
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_032_remove_root_1(self):
        keys = [50, ]
        tree = self.TREE_CLASS.fromkeys(keys)
        del tree[50]
        self.assertTrue(tree.is_empty)

    def test_033_remove_root_2(self):
        keys = [50, 25, 12, 33, 34]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_034_remove_root_3(self):
        keys = [50, 25, 12, 33, 34, 75]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_035_remove_root_4(self):
        keys = [50, 25, 12, 33, 34, 75, 60]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_036_remove_root_5(self):
        keys = [50, 25, 12, 33, 34, 75, 60, 61]
        tree = self.TREE_CLASS.fromkeys(keys)
        remove_key = 50
        del tree[remove_key]
        self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_037a_discard(self):
        keys = [50, 25, 12, 33, 34, 75, 60, 61]
        tree = self.TREE_CLASS.fromkeys(keys)
        try:
            tree.discard(17)
        except KeyError:
            self.assertTrue(False, "Discard raises KeyError")

    def test_037b_remove_keyerror(self):
        keys = [50, 25, 12, 33, 34, 75, 60, 61]
        tree = self.TREE_CLASS.fromkeys(keys)
        self.assertRaises(KeyError, tree.remove, 17)

    def test_038_remove_shuffeld(self):
        keys = [50, 25, 20, 35, 22, 23, 27, 75, 65, 90, 60, 70, 85, 57, 83, 58]
        remove_keys = keys[:]
        shuffle(remove_keys)
        for remove_key in remove_keys:
            tree = self.TREE_CLASS.fromkeys(keys)
            del tree[remove_key]
            self.assertTrue(check_integrity(keys, remove_key, tree))

    def test_039_remove_random_numbers(self):
        try:
            fp = open('xtestkey.txt')
            keys = eval(fp.read())
            fp.close()
        except IOError:
            keys = randomkeys(1000)
        shuffle(keys)
        tree = self.TREE_CLASS.fromkeys(keys)
        self.assertEqual(len(tree), len(keys))
        for key in keys:
            del tree[key]
        self.assertEqual(len(tree), 0)

    def test_040_sort_order(self):
        keys = randomkeys(1000)
        tree = self.TREE_CLASS.fromkeys(keys)
        generator = iter(tree)
        a = next(generator)
        for b in generator:
            self.assertTrue(b > a)
            a = b

    def test_041_pop(self):
        tree = self.TREE_CLASS(self.default_values2)
        data = tree.pop(8)
        self.assertEqual(data, 45)
        self.assertFalse(8 in tree)
        self.assertRaises(KeyError, tree.pop, 8)
        self.assertEqual(tree.pop(8, 99), 99)

    def test_042_popitem(self):
        tree = self.TREE_CLASS(self.default_values2)
        d = dict()
        while not tree.is_empty():
            key, value = tree.popitem()
            d[key] = value
        expected = {2: 12, 4: 34, 8: 45, 1: 16, 9: 35, 3: 57}
        self.assertEqual(expected, d)
        self.assertRaises(KeyError, tree.popitem)

    def test_043_min_item(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        min_item = tree.min_item()
        self.assertEqual(min_item[1], 0)

    def test_044_min_item_error(self):
        tree = self.TREE_CLASS()
        self.assertRaises(ValueError, tree.min_item)

    def test_045_max_item(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        max_item = tree.max_item()
        self.assertEqual(max_item[1], 999)

    def test_046_max_item_error(self):
        tree = self.TREE_CLASS()
        self.assertRaises(ValueError, tree.max_item)

    def test_047_min_key(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        minkey = tree.min_key()
        self.assertEqual(minkey, 0)
        self.assertEqual(minkey, min(tree))

    def test_048_min_key_error(self):
        tree = self.TREE_CLASS()
        self.assertRaises(ValueError, tree.min_key)

    def test_049_max_key(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        maxkey = tree.max_key()
        self.assertEqual(maxkey, 999)
        self.assertEqual(maxkey, max(tree))

    def test_050_min_key_error(self):
        tree = self.TREE_CLASS()
        self.assertRaises(ValueError, tree.max_key)

    def test_051_prev_item(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        prev_value = None
        for key in tree.keys():
            try:
                prev_item = tree.prev_item(key)
            except KeyError:  # only on first key
                self.assertEqual(prev_value, None)
            if prev_value is not None:
                self.assertEqual(prev_value, prev_item[1])
            prev_value = key

    def test_052_prev_key_extreme(self):
        # extreme degenerated binary tree (if unbalanced)
        tree = self.TREE_CLASS.fromkeys([1, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
        self.assertEqual(tree.prev_key(2), 1)

    def test_053_prev_item_error(self):
        tree = self.TREE_CLASS()
        tree[0] = 'NULL'
        self.assertRaises(KeyError, tree.prev_item, 0)

    def test_054_succ_item(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        succ_value = None
        for key in tree.keys(reverse=True):
            try:
                succ_item = tree.succ_item(key)
            except KeyError:  # only on last key
                self.assertEqual(succ_value, None)
            if succ_value is not None:
                self.assertEqual(succ_value, succ_item[1])
            succ_value = key

    def test_055_succ_key_extreme(self):
        # extreme degenerated binary tree (if unbalanced)
        tree = self.TREE_CLASS.fromkeys([15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(tree.succ_key(10), 15)

    def test_056_succ_item_error(self):
        tree = self.TREE_CLASS()
        tree[0] = 'NULL'
        self.assertRaises(KeyError, tree.succ_item, 0)

    def test_057_prev_key(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        pkey = None
        for key in tree.keys():
            try:
                prev_key = tree.prev_key(key)
            except KeyError:  # only on first key
                self.assertEqual(pkey, None)
            if pkey is not None:
                self.assertEqual(pkey, prev_key)
            pkey = key

    def test_058_prev_key_error(self):
        tree = self.TREE_CLASS()
        tree[0] = 'NULL'
        self.assertRaises(KeyError, tree.prev_key, 0)

    def test_059_succ_key(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        skey = None
        for key in tree.keys(reverse=True):
            try:
                succ_key = tree.succ_key(key)
            except KeyError:  # only on last key
                self.assertEqual(skey, None)
            if skey is not None:
                self.assertEqual(skey, succ_key)
            skey = key

    def test_060_succ_key_error(self):
        tree = self.TREE_CLASS()
        tree[0] = 'NULL'
        self.assertRaises(KeyError, tree.succ_key, 0)

    def test_061_prev_succ_on_empty_trees(self):
        tree = self.TREE_CLASS()
        self.assertRaises(KeyError, tree.succ_key, 0)
        self.assertRaises(KeyError, tree.prev_key, 0)
        self.assertRaises(KeyError, tree.succ_item, 0)
        self.assertRaises(KeyError, tree.prev_item, 0)

    def test_062_succ_prev_key_random_1000(self):
        keys = list(set([randint(0, 10000) for _ in range(1000)]))
        shuffle(keys)
        tree = self.TREE_CLASS.fromkeys(keys)

        skey = None
        for key in tree.keys(reverse=True):
            try:
                succ_key = tree.succ_key(key)
            except KeyError:  # only on last key
                self.assertEqual(skey, None)
            if skey is not None:
                self.assertEqual(skey, succ_key)
            skey = key

        pkey = None
        for key in tree.keys():
            try:
                prev_key = tree.prev_key(key)
            except KeyError:  # only on first key
                self.assertEqual(pkey, None)
            if pkey is not None:
                self.assertEqual(pkey, prev_key)
            pkey = key

    def test_063_pop_min(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        keys = sorted(set3[:])
        for key in keys:
            k, v = tree.pop_min()
            self.assertEqual(key, v)

    def test_064_pop_min_error(self):
        tree = self.TREE_CLASS()
        self.assertRaises(ValueError, tree.pop_min)

    def test_065_pop_max(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        keys = sorted(set3[:], reverse=True)
        for key in keys:
            k, v = tree.pop_max()
            self.assertEqual(key, v)

    def test_066_pop_max_error(self):
        tree = self.TREE_CLASS()
        self.assertRaises(ValueError, tree.pop_max)

    def test_067_nlargest(self):
        l = list(range(30))
        shuffle(l)
        tree = self.TREE_CLASS(zip(l, l))
        result = tree.nlargest(10)
        chk = [(x, x) for x in range(29, 19, -1)]
        self.assertEqual(chk, result)

    def test_068_nlargest_gt_len(self):
        items = list(zip(range(5), range(5)))
        tree = self.TREE_CLASS(items)
        result = tree.nlargest(10)
        self.assertEqual(result, list(reversed(items)))

    def test_069_nsmallest(self):
        l = list(range(30))
        shuffle(l)
        tree = self.TREE_CLASS(zip(l, l))
        result = tree.nsmallest(10)
        chk = [(x, x) for x in range(0, 10)]
        self.assertEqual(chk, result)

    def test_070_nsmallest_gt_len(self):
        items = list(zip(range(5), range(5)))
        tree = self.TREE_CLASS(items)
        result = tree.nsmallest(10)
        self.assertEqual(result, items)

    def test_071_reversed(self):
        tree = self.TREE_CLASS(zip(set3, set3))
        result = reversed(sorted(set3))
        for key, chk in zip(reversed(tree), result):
            self.assertEqual(chk, key)

    def test_077_delslice(self):
        T = self.TREE_CLASS.fromkeys([1, 2, 3, 4, 8, 9])
        tree = T.copy()
        del tree[:2]
        self.assertEqual(list(tree.keys()), [2, 3, 4, 8, 9])
        tree = T.copy()
        del tree[1:3]
        self.assertEqual(list(tree.keys()), [3, 4, 8, 9])
        tree = T.copy()
        del tree[3:]
        self.assertEqual(list(tree.keys()), [1, 2])
        tree = T.copy()
        del tree[:]
        self.assertEqual(list(tree.keys()), [])

    def test_080_intersection(self):
        l1 = list(range(30))
        shuffle(l1)
        l2 = list(range(15, 45))
        shuffle(l2)
        tree1 = self.TREE_CLASS(zip(l1, l1))
        tree2 = self.TREE_CLASS(zip(l2, l2))
        i = tree1 & tree2
        self.assertEqual(len(i), 15)
        self.assertEqual(i.min_key(), 15)
        self.assertEqual(i.max_key(), 29)

    def test_081_union(self):
        l1 = list(range(30))
        shuffle(l1)
        l2 = list(range(15, 45))
        shuffle(l2)
        tree1 = self.TREE_CLASS(zip(l1, l1))
        tree2 = self.TREE_CLASS(zip(l2, l2))
        i = tree1 | tree2
        self.assertEqual(len(i), 45)
        self.assertEqual(i.min_key(), 0)
        self.assertEqual(i.max_key(), 44)

    def test_082_difference(self):
        l1 = list(range(30))
        shuffle(l1)
        l2 = list(range(15, 45))
        shuffle(l2)

        tree1 = self.TREE_CLASS(zip(l1, l1))
        tree2 = self.TREE_CLASS(zip(l2, l2))
        i = tree1 - tree2
        self.assertEqual(len(i), 15)
        self.assertEqual(i.min_key(), 0)
        self.assertEqual(i.max_key(), 14)

    def test_083_symmetric_difference(self):
        l1 = list(range(30))
        shuffle(l1)
        l2 = list(range(15, 45))
        shuffle(l2)

        tree1 = self.TREE_CLASS(zip(l1, l1))
        tree2 = self.TREE_CLASS(zip(l2, l2))
        i = tree1 ^ tree2
        self.assertEqual(len(i), 30)
        self.assertEqual(i.min_key(), 0)
        self.assertEqual(i.max_key(), 44)
        self.assertTrue(15 not in i)
        self.assertTrue(29 not in i)

    @unittest.skipIf(PYPY, "getrefcount() not supported by pypy.")
    def test_084_refcount_get(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        tree[700] = 701
        chk = tree[700]
        count = sys.getrefcount(chk)
        for _ in range(10):
            chk = tree[700]

        self.assertEqual(sys.getrefcount(chk), count)

    @unittest.skipIf(PYPY, "getrefcount() not supported by pypy.")
    def test_085_refcount_set(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        chk = 800
        count = sys.getrefcount(chk)
        tree[801] = chk
        self.assertEqual(sys.getrefcount(chk), count + 1)

    @unittest.skipIf(PYPY, "getrefcount() not supported by pypy.")
    def test_086_refcount_del(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        chk = 900
        count = sys.getrefcount(chk)
        tree[901] = chk
        self.assertEqual(sys.getrefcount(chk), count + 1)
        del tree[901]
        self.assertEqual(sys.getrefcount(chk), count)

    @unittest.skipIf(PYPY, "getrefcount() not supported by pypy.")
    def test_087_refcount_replace(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        chk = 910
        count = sys.getrefcount(chk)
        tree[911] = chk
        self.assertEqual(sys.getrefcount(chk), count + 1)
        tree[911] = 912  # replace 910 with 912
        self.assertEqual(sys.getrefcount(chk), count)

    def test_088_pickle_protocol(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        pickle_str = pickle.dumps(tree, -1)
        tree2 = pickle.loads(pickle_str)
        self.assertEqual(len(tree), len(tree2))
        self.assertEqual(list(tree.keys()), list(tree2.keys()))
        self.assertEqual(list(tree.values()), list(tree2.values()))

    # [12, 34, 45, 16, 35, 57]
    def test_089_floor_item(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        self.assertEqual(tree.floor_item(12), (12, 12))
        self.assertEqual(tree.floor_item(13), (12, 12))
        self.assertEqual(tree.floor_item(60), (57, 57))

    def test_090a_floor_item_key_error(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        with self.assertRaises(KeyError):
            tree.floor_item(11)

    def test_090b_floor_item_empty_tree(self):
        tree = self.TREE_CLASS()
        with self.assertRaises(KeyError):
            tree.floor_item(11)

    def test_091_floor_key(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        self.assertEqual(tree.floor_key(12), 12)
        self.assertEqual(tree.floor_key(13), 12)
        self.assertEqual(tree.floor_key(60), 57)

    def test_092_floor_key_key_error(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        with self.assertRaises(KeyError):
            tree.floor_key(11)

    def test_093_ceiling_item(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        self.assertEqual(tree.ceiling_item(57), (57, 57))
        self.assertEqual(tree.ceiling_item(56), (57, 57))
        self.assertEqual(tree.ceiling_item(0), (12, 12))

    def test_094a_ceiling_item_key_error(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        with self.assertRaises(KeyError):
            tree.ceiling_item(60)

    def test_094a_ceiling_item_empty_tree(self):
        tree = self.TREE_CLASS()
        with self.assertRaises(KeyError):
            tree.ceiling_item(60)

    def test_095_ceiling_key(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        self.assertEqual(tree.ceiling_key(57), 57)
        self.assertEqual(tree.ceiling_key(56), 57)
        self.assertEqual(tree.ceiling_key(0), 12)

    def test_096_ceiling_key_key_error(self):
        tree = self.TREE_CLASS(self.default_values1)  # key == value
        with self.assertRaises(KeyError):
            tree.ceiling_key(60)


class TestBinaryTree(CheckTree, unittest.TestCase):
    TREE_CLASS = BinaryTree


class TestAVLTree(CheckTree, unittest.TestCase):
    TREE_CLASS = AVLTree


class TestRBTree(CheckTree, unittest.TestCase):
    TREE_CLASS = RBTree


class TestFastBinaryTree(CheckTree, unittest.TestCase):
    TREE_CLASS = FastBinaryTree


class TestFastAVLTree(CheckTree, unittest.TestCase):
    TREE_CLASS = FastAVLTree


class TestFastRBTree(CheckTree, unittest.TestCase):
    TREE_CLASS = FastRBTree

if __name__ == '__main__':
    unittest.main()
