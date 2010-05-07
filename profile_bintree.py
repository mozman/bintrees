#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile BinaryTree, FastBinaryTree
# Created: 01.05.2010

from timeit import Timer
from bintrees import BinaryTree
from bintrees import FastBinaryTree
from bintrees import QuickBinaryTree
from random import shuffle

COUNT = 100
KEYS = 5000
KEYRANGE = 1000000

setup_BinaryTree = """
from __main__ import bintree_build_delete, bintree_build, bintree_search
"""
setup_FastBinaryTree = """
from __main__ import cbintree_build_delete, cbintree_build, cbintree_search
"""
setup_QuickBinaryTree = """
from __main__ import qbintree_build_delete, qbintree_build, qbintree_search
"""

setup_FastBinaryTree_swc = """
from __main__ import keys, cbintree_wc_search, cy_wc_searchtree
"""

def random_keys():
    from random import shuffle, randint
    keys = set()
    while len(keys) < KEYS:
        keys.add(randint(0, KEYRANGE))
    keys = list(keys)
    shuffle(keys)
    return keys
try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    keys = random_keys()

py_searchtree = BinaryTree.fromkeys(keys)
cy_searchtree = FastBinaryTree.fromkeys(keys)
qt_searchtree = QuickBinaryTree.fromkeys(keys)

cy_wc_searchtree = FastBinaryTree.fromkeys(sorted(keys))


def bintree_build_delete():
    tree = BinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def cbintree_build_delete():
    tree = FastBinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def qbintree_build_delete():
    tree = QuickBinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def bintree_build():
    tree = BinaryTree.fromkeys(keys)

def cbintree_build():
    tree = FastBinaryTree.fromkeys(keys)

def qbintree_build():
    tree = QuickBinaryTree.fromkeys(keys)

def bintree_search():
    for key in keys:
        obj = py_searchtree[key]

def cbintree_search():
    for key in keys:
        obj = cy_searchtree[key]

def qbintree_search():
    for key in keys:
        obj = qt_searchtree.get_value(key)

def cbintree_wc_search():
    for key in keys:
        obj = cy_wc_searchtree[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("bintree_build()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree build only')

    t = Timer("cbintree_build()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree build only')

    t = Timer("qbintree_build()", setup_QuickBinaryTree)
    print_result(t.timeit(COUNT), 'QuickBinaryTree build only')

    t = Timer("bintree_build_delete()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree build & delete')

    t = Timer("cbintree_build_delete()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree build & delete')

    t = Timer("qbintree_build_delete()", setup_QuickBinaryTree)
    print_result(t.timeit(COUNT), 'QuickBinaryTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("bintree_search()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree search')

    t = Timer("cbintree_search()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree search')

    t = Timer("qbintree_search()", setup_QuickBinaryTree)
    print_result(t.timeit(COUNT), 'QuickBinaryTree search')

    #t = Timer("cbintree_wc_search()", setup_FastBinaryTree_swc)
    #print_result(t.timeit(COUNT), 'FastBinaryTree (worst case input: sorted keys) search')

if __name__=='__main__':
    main()