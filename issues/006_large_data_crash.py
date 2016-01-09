from random import randint
import bintrees


class HyperGraph:
    def __init__(self):
        self.alerts = []
        for x in range(0, 3000):
            alert = []
            for y in range(0, 6):
                alert.append(repr(randint(0, 7)))
            self.alerts.append(alert)
        self.hyper_dict = {}
        self.hcombinations = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4),
                              (2, 5), (3, 4), (3, 5), (4, 5)]
        for alert in self.alerts:
            for c in self.hcombinations:
                key = alert[:]
                for x in range(2):
                    key[c[x]] = '*'
                hyperkey = tuple(key)
                if hyperkey in self.hyper_dict:
                    self.hyper_dict[hyperkey].alerts.get(("test1", "test2"))
                else:
                    self.hyper_dict[hyperkey] = Hyperedge(key)

        for alert in self.alerts:
            for c in self.hcombinations:
                tmpkey = alert[:]
                for x in range(2):
                    tmpkey[c[x]] = '*'
                tmpkey = tuple(tmpkey)
                if tmpkey in self.hyper_dict:
                    del (self.hyper_dict[tmpkey])


class Hyperedge:
    def __init__(self, hyperkey):
        self.hyperkey = hyperkey
        self.alerts = bintrees.FastRBTree()
        self.alerts.insert(("test1", "test2"), 1) # replace list by tuple -> no crash


for x in range(10):
    alertgraph = HyperGraph()
    print("finished iteration {} of 10".format(x))
