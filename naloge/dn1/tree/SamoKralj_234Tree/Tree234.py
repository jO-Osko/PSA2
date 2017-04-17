# -*- coding: utf-8 -*-

from tree.AbstractTree import AbstractTree

__author__ = 'Samo Kralj'

class Tree_234(AbstractTree):
    def __init__(self):
        self.koren = Node()

    def search(self, k):

        def find(self, k, node):
            for i in range(len(node.key)):
                tip, value = node.key[i]
                if tip == 'V':
                    if value == k:
                        return True, node
                    if value > k:
                        if node.key[i-1][1] is not None:
                            return find(self, k, node.key[i-1][1])
                        else:
                            return False, node
            return False, node
        
        return find(self, k, self.koren)
        
class Node():
    def __init__(self, value = None, parent = None):
        self.keys = []
        self.childs = [None]
        self.parent = parent
        

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
            print(self)
            pushup = self.keys[2]
            #LEVO = Node()
            #LEVO.keys = self.keys[:2][:]
            #LEVO.childs = self.childs[:3][:]
            DESNO = Node()
            DESNO.keys = self.keys[3:][:]
            DESNO.childs = self.childs[3:][:]
            self.keys = self.keys[:2][:]
            self.childs = self.childs[:3][:]
            print(self)
            print(DESNO)
            if self.parent is not None:
                #LEVO.parent = self.parent
                DESNO.parent = self.parent
                self.parent.add(pushup, repair = False)
                ind = self.parent.indeks(pushup)
                self.parent.childs[ind] = self
                self.parent.childs[ind+1] = DESNO
            else:
                parent = Node()
                self.parent = parent
                #LEVO.parent = parent
                DESNO.parent = parent
                parent.add(pushup, repair = False)
                parent.childs[0] = self
                parent.childs[1] = DESNO
            self.parent.repair()
            

    def remove(self, value):
        pass
                        
                
            
            
