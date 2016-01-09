#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile RBTree, FastRBTree
# Created: 17.05.2013
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

import sys
from timeit import Timer

from bintrees import RBTree as PTree
from bintrees import FastRBTree as FTree, has_fast_tree_support

COUNT = 100

setup_RBTree_ps = """
from __main__ import rb_iter_by_prev_item, rb_iter_by_succ_item, rb_iter_by_item_slice_prev, rb_iter_by_item_slice_succ
"""
setup_FastRBTree_ps = """
from __main__ import crb_iter_by_prev_item, crb_iter_by_succ_item, crb_iter_by_item_slice_prev, crb_iter_by_item_slice_succ
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

ptree = PTree.from_keys(keys)
ftree = FTree.from_keys(keys)
sorted_keys = list(ftree.keys())
median_key = sorted_keys[int(len(sorted_keys) / 2)]


def rb_iter_by_prev_item():
    key = median_key
    while True:
        try:
            key, value = ptree.prev_item(key)
        except KeyError:
            break


def rb_iter_by_succ_item():
    key = median_key
    while True:
        try:
            key, value = ptree.succ_item(key)
        except KeyError:
            break


def rb_iter_by_item_slice_prev():
    for item in ptree.iter_items(None, median_key):
        pass


def rb_iter_by_item_slice_succ():
    for item in ptree.iter_items(median_key, None):
        pass


def crb_iter_by_prev_item():
    key = median_key
    while True:
        try:
            key, value = ftree.prev_item(key)
        except KeyError:
            break


def crb_iter_by_succ_item():
    key = median_key
    while True:
        try:
            key, value = ftree.succ_item(key)
        except KeyError:
            break


def crb_iter_by_item_slice_prev():
    for item in ftree.iter_items(None, median_key):
        pass


def crb_iter_by_item_slice_succ():
    for item in ftree.iter_items(median_key, None):
        pass


def print_result(time, text):
    print("Operation: %s == [ %.2f s ]\n" % (text, time))


def main():
    print ("Iterating {}x {} keys out of {} Nodes.\n".format(COUNT, len(keys)/2, len(keys)))

    t = Timer("rb_iter_by_prev_item()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'RBTree iterating by k, v = prev_item(k)')

    t = Timer("rb_iter_by_succ_item()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'RBTree iterating by k, v = succ_item(k)')

    t = Timer("rb_iter_by_item_slice_prev()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'RBTree itemslice(None, median_key)')

    t = Timer("rb_iter_by_item_slice_succ()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'RBTree itemslice(median_key: None)')

    t = Timer("crb_iter_by_prev_item()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastRBTree iterating by k, v = prev_item(k)')

    t = Timer("crb_iter_by_succ_item()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastRBTree iterating by k, v = succ_item(k)')

    t = Timer("crb_iter_by_item_slice_prev()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastRBTree itemslice(None, median_key)')

    t = Timer("crb_iter_by_item_slice_succ()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastRBTree itemslice(median_key, None)')

if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastRBTree is NOT working.")
    else:
        print("Cython extension for FastRBTree is working.")
    main()
