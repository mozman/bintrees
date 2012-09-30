#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile memory usage of FastBinaryTree, FastRBTree and FastAVLTree compared with dict
# Created: 02.05.2010

from guppy import hpy
hp=hpy()

from bintrees import FastBinaryTree
from bintrees import FastAVLTree
from bintrees import FastRBTree

from bintrees import BinaryTree
from bintrees import AVLTree
from bintrees import RBTree

COUNT = 100

try:
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()

except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

def main():
    log = open("memory_usage.txt", 'w')
    log.write("Initial memory usage:\n\n")
    log.write(str(hp.heap()))
    log.write("\n\nCreating {0} dicts with {1} objects:\n".format(COUNT, len(keys)))
    dicts = [dict.fromkeys(keys) for _ in xrange(COUNT)]

    log.write("Creating {0} Cython FastBinaryTrees with {1} objects:\n".format(COUNT, len(keys)))
    bintrees = [FastBinaryTree.fromkeys(keys) for _ in xrange(COUNT)]

    log.write("Creating {0} Cython FastAVLTrees with {1} objects:\n".format(COUNT, len(keys)))
    avltrees = [FastAVLTree.fromkeys(keys) for _ in xrange(COUNT)]

    log.write("Creating {0} Cython FastRBTrees with {1} objects:\n\n".format(COUNT, len(keys)))
    rbtrees = [FastRBTree.fromkeys(keys) for _ in xrange(COUNT)]

    log.write("Creating {0} Python BinaryTrees with {1} objects:\n".format(COUNT, len(keys)))
    pbintrees = [BinaryTree.fromkeys(keys) for _ in xrange(COUNT)]

    log.write("Creating {0} Python AVLTrees with {1} objects:\n".format(COUNT, len(keys)))
    pavltrees = [AVLTree.fromkeys(keys) for _ in xrange(COUNT)]

    log.write("Creating {0} Python RBTrees with {1} objects:\n\n".format(COUNT, len(keys)))
    prbtrees = [RBTree.fromkeys(keys) for _ in xrange(COUNT)]

    log.write(str(hp.heap()))
    log.close()

if __name__=='__main__':
    main()