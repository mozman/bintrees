#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile AVLTree, cAVLTree
# Created: 01.05.2010

from timeit import Timer
from bintrees.avltree import AVLTree
from bintrees.cavltree import cAVLTree

COUNT = 100

setup_AVLTree_bd = """
from __main__ import keys, profile_avltree_bd
"""
setup_cAVLTree_bd = """
from __main__ import keys, profile_cavltree_bd
"""
setup_AVLTree_b = """
from __main__ import keys, profile_avltree_b
"""
setup_cAVLTree_b = """
from __main__ import keys, profile_cavltree_b
"""

def random_keys():
    from random import shuffle, randint
    keys = list(set([randint(0, 10000) for _ in xrange(1000)]))
    shuffle(keys)
    return keys

keys = random_keys()

def profile_avltree_bd():
    from bintrees.avltree import AVLTree
    tree = AVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_cavltree_bd():
    from bintrees.cavltree import cAVLTree
    tree = cAVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def profile_avltree_b():
    from bintrees.avltree import AVLTree
    tree = AVLTree.fromkeys(keys)

def profile_cavltree_b():
    from bintrees.cavltree import cAVLTree
    tree = cAVLTree.fromkeys(keys)

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    t = Timer("profile_avltree_b()", setup_AVLTree_b)
    print_result(t.timeit(COUNT), 'AVLTree build only')

    t = Timer("profile_cavltree_b()", setup_cAVLTree_b)
    print_result(t.timeit(COUNT), 'cAVLTree build only')

    t = Timer("profile_avltree_bd()", setup_AVLTree_bd)
    print_result(t.timeit(COUNT), 'AVLTree build & delete')

    t = Timer("profile_cavltree_bd()", setup_cAVLTree_bd)
    print_result(t.timeit(COUNT), 'cAVLTree build & delete')

if __name__=='__main__':
    main()