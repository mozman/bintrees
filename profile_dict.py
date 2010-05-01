#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile BinaryTree, cBinaryTree
# Created: 01.05.2010

from timeit import Timer
from bintrees.cbintree import cBinaryTree
from bintrees.cavltree import cAVLTree

COUNT = 100
KEYS = 5000

setup_Dict_bd = """
from __main__ import keys, profile_dict_bd
"""
setup_cBinaryTree_bd = """
from __main__ import keys, profile_cbintree_bd
"""
setup_Dict_b = """
from __main__ import keys, profile_dict_b
"""
setup_cBinaryTree_b = """
from __main__ import keys, profile_cbintree_b
"""
setup_cAVLTree_bd = """
from __main__ import keys, profile_cavltree_bd
"""
setup_cAVLTree_b = """
from __main__ import keys, profile_cavltree_b
"""

def random_keys():
    from random import shuffle, randint
    keys = list(set([randint(0, 1000000) for _ in xrange(KEYS)]))
    shuffle(keys)
    return keys

keys = random_keys()

def profile_dict_bd():
    tree = dict.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_cbintree_bd():
    from bintrees.cbintree import cBinaryTree
    tree = cBinaryTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_dict_b():
    tree = dict.fromkeys(keys)

def profile_cbintree_b():
    from bintrees.cbintree import cBinaryTree
    tree = cBinaryTree.fromkeys(keys)

def profile_cavltree_bd():
    from bintrees.cavltree import cAVLTree
    tree = cAVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_cavltree_b():
    from bintrees.cavltree import cAVLTree
    tree = cAVLTree.fromkeys(keys)

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    t = Timer("profile_dict_b()", setup_Dict_b)
    print_result(t.timeit(COUNT), 'dict() build only')

    t = Timer("profile_cbintree_b()", setup_cBinaryTree_b)
    print_result(t.timeit(COUNT), 'cBinaryTree build only')

    t = Timer("profile_cavltree_b()", setup_cAVLTree_b)
    print_result(t.timeit(COUNT), 'cAVLTree build only')

    t = Timer("profile_dict_bd()", setup_Dict_bd)
    print_result(t.timeit(COUNT), 'dict() build & delete')

    t = Timer("profile_cbintree_bd()", setup_cBinaryTree_bd)
    print_result(t.timeit(COUNT), 'cBinaryTree build & delete')

    t = Timer("profile_cavltree_bd()", setup_cAVLTree_bd)
    print_result(t.timeit(COUNT), 'cAVLTree build & delete')

if __name__=='__main__':
    main()