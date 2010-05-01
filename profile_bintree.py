#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile BinaryTree, cBinaryTree
# Created: 01.05.2010

from timeit import Timer
from bintrees.bintree import BinaryTree
from bintrees.cbintree import cBinaryTree

COUNT = 100

setup_BinaryTree_bd = """
from __main__ import keys, profile_bintree_bd
"""
setup_cBinaryTree_bd = """
from __main__ import keys, profile_cbintree_bd
"""
setup_BinaryTree_b = """
from __main__ import keys, profile_bintree_b
"""
setup_cBinaryTree_b = """
from __main__ import keys, profile_cbintree_b
"""

def random_keys():
    from random import shuffle, randint
    keys = list(set([randint(0, 10000) for _ in xrange(1000)]))
    shuffle(keys)
    return keys

keys = random_keys()

def profile_bintree_bd():
    from bintrees.bintree import BinaryTree
    tree = BinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_cbintree_bd():
    from bintrees.cbintree import cBinaryTree
    tree = cBinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_bintree_b():
    from bintrees.bintree import BinaryTree
    tree = BinaryTree.fromkeys(keys)

def profile_cbintree_b():
    from bintrees.cbintree import cBinaryTree
    tree = cBinaryTree.fromkeys(keys)

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    t = Timer("profile_bintree_b()", setup_BinaryTree_b)
    print_result(t.timeit(COUNT), 'BinaryTree build only')

    t = Timer("profile_cbintree_b()", setup_cBinaryTree_b)
    print_result(t.timeit(COUNT), 'cBinaryTree build only')

    t = Timer("profile_bintree_bd()", setup_BinaryTree_bd)
    print_result(t.timeit(COUNT), 'BinaryTree build & delete')

    t = Timer("profile_cbintree_bd()", setup_cBinaryTree_bd)
    print_result(t.timeit(COUNT), 'cBinaryTree build & delete')

if __name__=='__main__':
    main()