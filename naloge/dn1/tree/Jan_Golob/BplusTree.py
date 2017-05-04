from enum import Enum
from typing import TypeVar, Iterable, Optional, Generic, Union, Iterator

from ..AbstractTree import AbstractSearchTree

__author__ = "Jan Golob"

T = TypeVar("T")



class LeafNode:
    def __init__(self, b, parent=None, data=[]):
        self.b = b
        self.parent = parent
        self.leaf = True
        self.data = data
        self.len = len(data)
        self.next = None

    def tree_search(self, k):
        return self

    def insert(self, k, val):
        self.add(k, val)
        self.len += 1
        if self.len >= self.b:
            self.split()

    def add(self, k, val):
        for i,l in enumerate(self.data):
            if l[0] >= k:
                self.data.insert(i, (k, val))
                return
        self.data.append((k, val))

    def search(self, k, val):
        for ent in self.data:
            i, vl = ent
            if i == k:
                if vl == val:
                    return True
            elif i > k:
                return False
        if self.next is not None:
            return self.next.search(k, val)
        else:
            return False

    def split(self):
        split_i = self.len // 2
        k = self.data[split_i][0]
        if self.parent is not None:
            right = LeafNode(self.b, self.parent, self.data[split_i:])
            self.data = self.data[0: split_i]
            self.next = right
            self.len = split_i
            self.parent.insert(k, right)



    def remove(self, k, val):
        i = self.delete(k, val)
        self.len -= 1
        if self.len < self.b//2:
            if self.next is not None:
                right = self.next
                if right.len <= self.b//2:
                    self.data += right.data
                    self.len += right.len
                    self.next = right.next
                    self.parent.remove(right)
                else:
                    self.data.append(right.data[0])
                    self.len +=1
                    right.data.__delitem__(0)
                    right.len -=1
                    self.parent.fixindex(right, right.data[0])


    def delete(self, k, val):
        for i,ent in enumerate(self.data):
            l, vl = ent
            if l == k:
                if vl == val:
                    self.data.__delitem__(i)
                    return i
            elif l > k:
                raise FileNotFoundError
        if self.next is not None:
            return self.next.search(k, val)
        else:
            raise FileNotFoundError


    def __repr__(self):
       return 'L' + self.data[0:self.len].__repr__() + ' '



class InternalNode:
    def __init__(self, b, parent=None, keys=[], children=[]):
        self.b = b
        self.parent = parent
        self.leaf = False
        self.keys = keys
        self.children = children
        self.len = len(children)

    def tree_search(self, k):
        i = 0
        for l in self.keys:
            if k < l:
                return self.children[i].tree_search(k)
            i += 1
        return self.children[i].tree_search(k)

    def insert(self, k, val):
        self.add(k, val)
        self.len += 1
        if self.len > self.b:
            self.split()

    def add(self, k, val):
        for i, l in enumerate(self.keys):
            if l >= k:
                self.keys.insert(i, k)
                self.children.insert(i+1, val)
                return
        self.keys.append(k)
        self.children.append(val)

    def split(self):
        split_i = self.len // 2
        k = self.keys[split_i]
        if self.parent is not None:
            right = InternalNode(self.b, self.parent, self.keys[split_i + 1], self.children[split_i:])
            self.keys = self.keys[0: split_i - 1]
            self.children = self.children[0: split_i]
            self.len = split_i
            self.parent.insert(k, right)
            self.next = right
        else:
            right = InternalNode(self.b, self,  self.keys[split_i + 1:], self.children[split_i:])
            left = InternalNode(self.b, self,  self.keys[0: split_i - 1], self.children[0: split_i])
            self.keys = [k]
            self.len = 2
            self.children = [left, right]
            self.next = None
            left.next = right


    def fixindex(self, node, k):
        for i, val in enumerate(self.children):
            if val == node:
                self.keys[i-1]=k
                return

    def remove(self, node):
        self.delete(node)
        self.len -=1
        if self.parent is not None:
            if self.len < self.b//2:
                self.parent.merge()
            if self.parent.len == 1:
                self.parent.children = self.children

    def merge(self):
        for i, val in enumerate(self.children):
            if val.len//2:
                if self.children[i+1] is not None:
                    right = self.children[i + 1]
                    if self.children[i + 1].len < self.b//2:
                        val.keys += self.keys[i] + right.keys
                        self.keys.__delitem__(i)
                        val.children += right.children
                        val.len += right.len
                        self.remove(right)
                        self.len -=1
                    else:
                        val.data.append(right.data[0])
                        val.len += 1
                        right.data.__delitem__(0)
                        right.len -= 1
                        self.fixindex(right, right.data[0])





    def delete(self, node):
        for i, val in enumerate(self.children):
            if val == node:
                self.children.__delitem__(i)
                self.keys.__delitem__(i-1)
                return

    def __repr__(self):
        return '|'+repr(self.children)



class BplusTree(AbstractSearchTree):
    def __init__(self):
        b = 20
        assert b > 2
        self.root = InternalNode(b)
        self.root.children.append(LeafNode(b, self.root))
        # super().__init__(data)

    def insert(self, item):
        if not isinstance(item, tuple):
            (k,val) = (item, item)
        else:
            (k, val) = item
        self.root.tree_search(k).insert(k, val)



    def search(self, item):
        if not isinstance(item, tuple):
            (k,val) = (item, item)
        else:
            (k, val) = item
        return self.root.tree_search(k).search(k, val)


    def remove(self, item):
        if not isinstance(item, tuple):
            (k, val) = (item, item)
        else:
            (k, val) = item
        self.root.tree_search(k).remove(k, val)


