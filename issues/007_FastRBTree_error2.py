from random import randint
from bintrees import FastRBTree as Tree

class Hyperedge:
    def __init__(self, hyperkey, col, hlabel):
        self.hyperkey = hyperkey
        self.col = col
        self._alerts = Tree()
        self.insert_alert(hlabel, 1)
        self.nalerts = 1

    def get_alert(self, key):
        return self._alerts.get(key)

    def insert_alert(self, alert_key, count):
        self._alerts.insert(alert_key, count)

    def foreach_alert(self, func):
        self._alerts.foreach(func)

    def pop_alert(self, key):
        return self._alerts.pop(key)


def treeloop(hlabel, dupcount):
    alert = hyperedge.hyperkey[:]
    for x in range(2):
        alert[hyperedge.col[x]] = hlabel[x]
    for c in hcombinations:
        if hyperedge.col != c:
            label = []
            for x in range(2):
                label.append(alert[c[x]])
                alert[c[x]] = '*'
            tmpkey = tuple(alert)
            for x in range(2):
                alert[c[x]] = label[x]
            hlabel = tuple(label)
            if tmpkey in hyper_dict:
                tmpedge = hyper_dict[tmpkey]
                hypersize_list.discard((tmpedge.nalerts, tmpedge.hyperkey))
                tmpedge.nalerts -= tmpedge.pop_alert(hlabel)
                if tmpedge.nalerts > 0:
                    hypersize_list.insert((tmpedge.nalerts, tmpedge.hyperkey), tmpedge)


for z in range(10):
    hyper_dict = {}
    hypersize_list = Tree()
    hcombinations = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5),
                     (3, 4), (3, 5), (4, 5)]
    for x in range(0, 3000):
        alert = []
        for y in range(0, 6):
            alert.append(repr(randint(0, 8 - 1)) + "test")
        for c in hcombinations:
            label = []
            key = alert[:]
            for x in range(2):
                key[c[x]] = '*'
                label.append(alert[c[x]])

            hyperkey = tuple(key)
            hlabel = tuple(label)
            if hyperkey in hyper_dict:
                hyper_dict[hyperkey].nalerts += 1
                result = hyper_dict[hyperkey].get_alert(hlabel)
                if result is not None:
                    hyper_dict[hyperkey].insert_alert(hlabel, result + 1)
                else:
                    hyper_dict[hyperkey].insert_alert(hlabel, 1)
            else:
                hyper_dict[hyperkey] = Hyperedge(key, c, hlabel)

    for hyperedge in hyper_dict.values():
        hypersize_list.insert((hyperedge.nalerts, hyperedge.hyperkey), hyperedge)

    while not hypersize_list.is_empty():
        (key, hyperedge) = hypersize_list.pop_max()
        hyperedge.foreach_alert(treeloop)
    print("Completed iteration %d of 10" % z)
