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

setup_BinaryTree = """
from __main__ import bintree_build_delete, bintree_build, bintree_search
"""
setup_FastBinaryTree = """
from __main__ import cbintree_build_delete, cbintree_build, cbintree_search
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
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()
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

def qbintree_search():
    for key in keys:
        obj = qt_searchtree.get_value(key)

def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))

def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    t = Timer("bintree_build()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree build only')

    t = Timer("cbintree_build()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree build only')

    t = Timer("bintree_build_delete()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree build & delete')

    t = Timer("cbintree_build_delete()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("bintree_search()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree search')

    t = Timer("cbintree_search()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree search')

if __name__=='__main__':
    main()