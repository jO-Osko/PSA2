# -*- coding: utf-8 -*-

from tree.AbstractTree import AbstractTree

__author__ = 'Samo Kralj'

class Tree_234(AbstractTree):
    def __init__(self):
        self.koren = Node()

    def __repr__(self):
        return str(self.koren)

    def add(self, value):
        b, node = self.search(value)
        if not b:
            node.add(value)
            while self.koren.parent is not None:
                self.koren = self.koren.parent
        else:
            print('Element v drevesu že obstaja!')

    def search(self, k):

        def find(self, k, node):
            for i in range(len(node.keys)):
                value = node.keys[i]
                if value == k:
                    return True, node
                if value > k:
                    if node.childs[i] is not None:
                        return find(self, k, node.childs[i])
                    else:
                        return False, node
            if node.childs[-1] is not None:
                return find(self, k, node.childs[-1])
            else:
                return False, node
        
        return find(self, k, self.koren)

    def succ(self, k, node):
        if node.height > 0:
            ind = node.keys.index(k)
            v = node.childs[ind+1]
            while v.childs[0] is not None:
                v = v.childs[0]
            return v, v.keys[0]
            
    def remove(self, k):
        b, node = self.search(k)
        if not b:
            print('Element v drevesu ne obstaja!')
        else:
            if node.height > 0:
                v, nk = self.succ(k, node)
                in1 = node.keys.index(k)
                in2 = v.keys.index(nk)
                node.keys[in1] = nk
                v.keys[in2] = k
                v.remove(k)
            else:
                node.remove(k)
        
class Node():
    def __init__(self, value = None, parent = None):
        self.keys = []
        self.childs = [None]
        self.parent = parent
        self.height = 0
        

    def __repr__(self):
        return 'Keys: ' + str(self.keys) + ' Childs: ' + str(self.childs)

    def indeks(self, k):
        for i in range(len(self.keys)):
            if self.keys[i] == k:
                return i
        return False

    def add(self, value, repair = True):
        i = 0
        while i < len(self.keys) and self.keys[i] < value:
            i = i + 1
        self.keys = self.keys[:i] + [value] + self.keys[i:]
        if self.childs[i] is None:
            self.childs = self.childs[:i] + [None] + self.childs[i:]
        else:
            if self.childs[i].keys[0] > value:
                self.childs = self.childs[:i] + [None] + self.childs[i:]
            else:
                self.childs = self.childs[:i+1] + [None] + self.childs[i+1:]
        if repair:
            self.repair()

    def repair(self):
        if len(self.keys) > 3:
            pushup = self.keys[2]
            DESNO = Node()
            DESNO.keys = self.keys[3:][:]
            DESNO.childs = self.childs[3:][:]
            self.keys = self.keys[:2][:]
            self.childs = self.childs[:3][:]
            if self.parent is not None:
                DESNO.parent = self.parent
                self.parent.add(pushup, repair = False)
                ind = self.parent.indeks(pushup)
                self.parent.childs[ind] = self
                self.parent.childs[ind+1] = DESNO
            else:
                parent = Node()
                parent.height = self.height + 1
                self.parent = parent
                DESNO.parent = parent
                parent.add(pushup, repair = False)
                parent.childs[0] = self
                parent.childs[1] = DESNO
            self.parent.repair()
            

    def remove(self, value):
        self.keys.remove(value)
        self.childs.pop()
        
                        
                
            
            
