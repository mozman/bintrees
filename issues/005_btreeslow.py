import bintrees
import time

t = bintrees.FastRBTree.fromkeys(range(1000000), True)
start = 50000

key = start
t0 = time.time()
while True:
    try:
        key, _ = t.succ_item(key)
    except KeyError:
        break
t1 = time.time()
print("Iterating using succ_item(): %f sec" % (t1-t0))


t0 = time.time()
for key, _ in t.item_slice(start, None):
    pass
t1 = time.time()
print("Iterating using item_slice(): %f sec" % (t1-t0))
