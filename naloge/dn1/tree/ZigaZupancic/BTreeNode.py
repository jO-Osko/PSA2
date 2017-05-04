# -*- coding: utf-8 -*-
__author__ = "Žiga Zupančič"


class BTreeNode:
    def __init__(self, keys=None, children=None, parent=None):
        self.parent = parent
        self.children = children
        if keys is not None:
            self.keys = keys
        else:
            self.keys = []
        if self.children is not None:
            assert len(keys) + 1 == len(children), "Number of children must be equal to number of keys + 1"

    def __str__(self):
        return "Keys: " + str(self.keys) + ", Children: " + str(self.children)

    def __repr__(self):
        return "Keys: " + str(self.keys) + ", Children: " + str(self.children)
