#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile AVLTree, cAVLTree
# Created: 01.05.2010
import sys
from timeit import Timer
from random import shuffle

from bintrees.avltree import AVLTree
from bintrees.cavltree import cAVLTree

COUNT = 100

setup_AVLTree_bd = """
from __main__ import keys, avl_build_delete, AVLTree
"""
setup_cAVLTree_bd = """
from __main__ import keys, cavl_build_delete, cAVLTree
"""
setup_AVLTree_b = """
from __main__ import keys, avl_build, AVLTree
"""
setup_cAVLTree_b = """
from __main__ import keys, cavl_build, cAVLTree
"""
setup_AVLTree_s = """
from __main__ import keys, avl_search, py_searchtree
"""
setup_cAVLTree_s = """
from __main__ import keys, cavl_search, cy_searchtree
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    print("create 'testkeys.txt' with profile_avl.py\n")
    sys.exit()

py_searchtree = AVLTree.fromkeys(keys)
cy_searchtree = cAVLTree.fromkeys(keys)

def avl_build_delete():
    tree = AVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def cavl_build_delete():
    tree = cAVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def avl_build():
    tree = AVLTree.fromkeys(keys)

def cavl_build():
    tree = cAVLTree.fromkeys(keys)

def avl_search():
    for key in keys:
        obj = py_searchtree[key]

def cavl_search():
    for key in keys:
        obj = cy_searchtree[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("avl_build()", setup_AVLTree_b)
    print_result(t.timeit(COUNT), 'AVLTree build only')

    t = Timer("cavl_build()", setup_cAVLTree_b)
    print_result(t.timeit(COUNT), 'cAVLTree build only')

    t = Timer("avl_build_delete()", setup_AVLTree_bd)
    print_result(t.timeit(COUNT), 'AVLTree build & delete')

    t = Timer("cavl_build_delete()", setup_cAVLTree_bd)
    print_result(t.timeit(COUNT), 'cAVLTree build & delete')
    # shuffle search keys
    shuffle(keys)
    t = Timer("avl_search()", setup_AVLTree_s)
    print_result(t.timeit(COUNT), 'AVLTree search')

    t = Timer("cavl_search()", setup_cAVLTree_s)
    print_result(t.timeit(COUNT), 'cAVLTree search')

if __name__=='__main__':
    main()