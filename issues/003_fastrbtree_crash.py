from bintrees import RBTree, FastRBTree

# Commenting in the first outcommented line in below function
# results in the trees being unequal and a KeyError occurring. They should
# not be unequal (the RBTree is correct)
# Commenting in further lines results in further discrepancies

def populate(tree):
    tree[14] = tree.get(14,0) + 212
    tree[15.84] = tree.get(15.84,0) + 623
    tree[16] = tree.get(16,0) + 693
    tree[16] = 1213
    tree[16.3] = tree.get(16.3,0) + 1952
    tree[15.8] = tree.get(15.8,0) + 1934
    tree[16.48] = tree.get(16.48,0) + 65
    tree[14.95] = tree.get(14.95,0) + 325
    tree[15.07] = tree.get(15.07,0) + 1293
    tree[16.41] = tree.get(16.41,0) + 2000
    tree[16.43] = tree.get(16.43,0) + 2000
    tree[16.45] = tree.get(16.45,0) + 2000
    tree[16.4] = tree.get(16.4,0) + 2000
    tree[16.42] = tree.get(16.42,0) + 2000
    tree[16.47] = tree.get(16.47,0) + 2000
    tree[16.44] = tree.get(16.44,0) + 2000
    tree[16.46] = tree.get(16.46,0) + 2000
    tree[16.48] = tree.get(16.48,0) + 2065
    tree[16.51] = tree.get(16.51,0) + 600
    tree[16.5] = tree.get(16.5,0) + 600
    tree[16.49] = tree.get(16.49,0) + 600
    tree[16.5] = 1400
    tree[16.49] = 2600
    tree[16.49] = 3159
    tree[16.47] = 2694
    tree[16.5] = 2079
    tree[16.48] = 2599
    tree[16.46] = 2564
    tree[16.44] = 2709
#    tree[16.45] = 2644
#    tree[16.43] = 2621
#    tree[16.49] = 3959
#    tree[16.47] = 3494
#    tree[16.48] = 3399
#    tree[16.46] = 3364
#    tree[16.44] = 3509
#    tree[16.45] = 3444
#    tree[16.43] = 3421
#    tree[16.46] = 3735
#    del tree[15.84]
#    tree[16.43] = 4921
#    tree[16.48] = 4099
#    tree[16.5] = 1279
#    tree[16.49] = 1959
#    tree[16.39] = tree.get(16.39,0) + 2000

rbt = RBTree()
frbt = FastRBTree()
populate(rbt)
populate(frbt)

print('RBT len: {0} FRBT len: {1}'.format(len(rbt), len(frbt)))
for key, value in rbt.items():
    print("RBTree[{key}] = {value} <-> FastRBTree[{key}] = {value2}".format(key=key, value=value, value2=frbt[key]))
