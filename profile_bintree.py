#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile BinaryTree, FastBinaryTree
# Created: 01.05.2010

from timeit import Timer
from bintrees import BinaryTree
from bintrees import FastBinaryTree
from random import shuffle

COUNT = 100
KEYS = 5000
KEYRANGE = 1000000

setup_BinaryTree_bd = """
from __main__ import keys, bintree_build_delete, BinaryTree
"""
setup_FastBinaryTree_bd = """
from __main__ import keys, cbintree_build_delete, FastBinaryTree
"""
setup_BinaryTree_b = """
from __main__ import keys, bintree_build, BinaryTree
"""
setup_FastBinaryTree_b = """
from __main__ import keys, cbintree_build, FastBinaryTree
"""
setup_BinaryTree_s = """
from __main__ import keys, bintree_search, py_searchtree
"""
setup_FastBinaryTree_s = """
from __main__ import keys, cbintree_search, cy_searchtree
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

def bintree_build_delete():
    tree = BinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def cbintree_build_delete():
    tree = FastBinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def bintree_build():
    tree = BinaryTree.fromkeys(keys)

def cbintree_build():
    tree = FastBinaryTree.fromkeys(keys)

def bintree_search():
    for key in keys:
        obj = py_searchtree[key]

def cbintree_search():
    for key in keys:
        obj = cy_searchtree[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("bintree_build()", setup_BinaryTree_b)
    print_result(t.timeit(COUNT), 'BinaryTree build only')

    t = Timer("cbintree_build()", setup_FastBinaryTree_b)
    print_result(t.timeit(COUNT), 'FastBinaryTree build only')

    t = Timer("bintree_build_delete()", setup_BinaryTree_bd)
    print_result(t.timeit(COUNT), 'BinaryTree build & delete')

    t = Timer("cbintree_build_delete()", setup_FastBinaryTree_bd)
    print_result(t.timeit(COUNT), 'FastBinaryTree build & delete')
    # shuffle search keys
    shuffle(keys)
    t = Timer("bintree_search()", setup_BinaryTree_s)
    print_result(t.timeit(COUNT), 'BinaryTree search')

    t = Timer("cbintree_search()", setup_FastBinaryTree_s)
    print_result(t.timeit(COUNT), 'FastBinaryTree search')

if __name__=='__main__':
    main()