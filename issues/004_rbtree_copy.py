'''
Created on Apr 11, 2013

@author: matthijssnel
'''

from bintrees import FastRBTree


def print_node(key, value):
    print("Key: {}; Value:{}".format(key, value))


def populate(tree):
    tree[20.5] = tree.get(20.5, 0) + 644
    tree[17.35] = tree.get(17.35, 0) + 32
    tree[19.5] = tree.get(19.5, 0) + 440
    tree[20.0] = tree.get(20.0, 0) + 73
    tree[18.5] = tree.get(18.5, 0) + 1500
    tree[20.8] = tree.get(20.8, 0) + 330
    tree[21.0] = tree.get(21.0, 0) + 450
    tree[19.25] = tree.get(19.25, 0) + 137
    tree[18.7] = tree.get(18.7, 0) + 740
    tree[20.12] = tree.get(20.12, 0) + 500
    tree[19.85] = tree.get(19.85, 0) + 300
    del tree[17.35]
    tree[18.5] = 1662
    tree[17.23] = tree.get(17.23, 0) + 4594
    tree[16.6] = tree.get(16.6, 0) + 2000
    tree[16.62] = tree.get(16.62, 0) + 2000
    tree[16.66] = tree.get(16.66, 0) + 2000
    tree[16.68] = tree.get(16.68, 0) + 2000
    tree[16.61] = tree.get(16.61, 0) + 2000
    tree[16.64] = tree.get(16.64, 0) + 2000
    tree[16.67] = tree.get(16.67, 0) + 2000
    tree[16.57] = tree.get(16.57, 0) + 600
    tree[16.58] = tree.get(16.58, 0) + 600
    tree[16.59] = tree.get(16.59, 0) + 600
    del tree[16.68]
    tree[16.59] = 2600
    tree[16.59] = 2000
    tree[16.56] = tree.get(16.56, 0) + 600
    tree[16.59] = 2800
    del tree[16.67]
    tree[16.58] = 2600
    tree[16.56] = 5796
    tree[16.56] = 600
    tree[16.57] = 2600
    tree[16.56] = 1400
    tree[16.55] = tree.get(16.55, 0) + 5196
    tree[16.53] = tree.get(16.53, 0) + 548
    tree[16.55] = 5829
    tree[16.54] = tree.get(16.54, 0) + 657
    tree[16.56] = 1964
    tree[16.58] = 3119
    tree[16.6] = 2691
    tree[16.57] = 3245
    tree[16.59] = 3385
    tree[16.58] = 3919
    tree[16.6] = 3491
    tree[16.57] = 4045
    del tree[16.66]
    tree[16.56] = 2764
    tree[16.55] = 6629
    tree[16.58] = 3319
    tree[16.55] = 7229
    tree[16.55] = 2033
    tree[16.55] = 2833
    tree[16.54] = 1457
    tree[16.54] = 6653
    tree[16.54] = 5996
    tree[16.62] = 2492
    del tree[16.53]
    tree[16.61] = 2708
    tree[16.54] = 5196
    tree[16.55] = 2033
    tree[16.62] = 2000
    tree[16.54] = 5801
    tree[16.62] = 2800
    tree[16.61] = 3508
    tree[16.58] = 3687
    tree[16.61] = 2800
    tree[16.53] = tree.get(16.53, 0) + 522
    tree[16.55] = 2833
    tree[16.54] = 6601
    tree[16.54] = 1405
    tree[16.53] = 5718
    tree[16.6] = 2800
    tree[16.52] = tree.get(16.52, 0) + 537
    tree[16.58] = 3319
    tree[16.56] = 3133
    tree.copy()
    del tree[16.52]
    tree[16.6] = 3471
    tree[16.6] = 2800
    tree[16.52] = tree.get(16.52, 0) + 655
    tree[16.54] = 2905
    tree[16.57] = 3445
    del tree[16.64]
    tree[16.54] = 3705
    tree[16.53] = 6518
    tree[16.59] = 2800
    tree[16.51] = tree.get(16.51, 0) + 523
    clone = tree.copy()
    print("\nOriginal Tree:")
    tree.foreach(print_node)
    print("\nClone Tree:")
    clone.foreach(print_node)


tree = FastRBTree()
populate(tree)

