# -*- coding: utf-8 -*-

from tree.AbstractTree import AbstractTree

__author__ = 'Samo Kralj'

class Tree_234(AbstractTree):
    def __init__(self, data = []):
        self.koren = Node()
        for el in data:
            self.add(el)

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
            raise ValueError('Element v drevesu ne obstaja!')
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
        if len(self.koren.keys) == 0:
            self.koren = self.koren.childs[0]
        
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
            for otrok in self.childs[3:]:
                if otrok is not None:
                    otrok.parent = DESNO
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
        if len(self.keys) > 1:
            self.keys.remove(value)
            self.childs.pop()
            return 
        if self.parent is not None:
            parent = self.parent
            glej = self.keys[0]
            ind = 0
            while ind < len(parent.keys) and parent.keys[ind] < glej:
                ind += 1
            if ind == 0:
                if len(parent.childs[1].keys) >= 2:
                    ro = parent.childs[1]
                    self.keys[0] = parent.keys[0]
                    parent.keys[0] = ro.keys[0]
                    ro.keys.pop(0)
                    ro.childs.pop()
                    return
            if ind == len(parent.keys):
                if len(parent.childs[ind-1].keys) >= 2:
                    lo = parent.childs[ind-1]
                    self.keys[0] = parent.keys[-1]
                    parent.keys[-1] = lo.keys[-1]
                    lo.keys.pop(-1)
                    lo.childs.pop()
                    return
            if 0 < ind < len(parent.keys):
                lo = parent.childs[ind-1]
                ro = parent.childs[ind+1]
                if len(lo.keys) >= 2:
                    self.keys[0] = parent.keys[ind-1]
                    parent.keys[ind-1] = lo.keys[-1]
                    lo.keys.pop(-1)
                    lo.childs.pop()
                    return
                if len(ro.keys) >= 2:
                    self.keys[0] = parent.keys[ind]
                    parent.keys[ind] = ro.keys[0]
                    ro.keys.pop(0)
                    ro.childs.pop()
                    return
            self.special(value)
        else:
            # V vozlišču je le ena vrednost in nimamo starša.
            self.keys.remove(value)
            self.childs.pop()

    def special(self, value):
        parent = self.parent
        ind = 0
        while ind < len(parent.keys) and parent.keys[ind] < value:
            ind += 1
        if ind == 0:
            self.keys[0] = parent.keys[0]
            zdruzi = parent.childs[1]
            self.keys.extend(zdruzi.keys)
            self.childs.extend(zdruzi.childs[1:])
            parent.keys.pop(0)
            parent.childs.pop(1)
        elif ind == len(parent.keys):
            zdruzi = parent.childs[ind-1]
            self.keys = zdruzi.keys[:] + [parent.keys[ind-1]]
            self.childs = zdruzi.childs + self.childs[1:]
            parent.keys.pop(-1)
            parent.childs.pop(-2)
        else:
            zdruzi = parent.childs[ind+1]
            self.keys = [parent.keys[ind]] + zdruzi.keys
            self.childs = self.childs + zdruzi.childs[1:]
            parent.keys.pop(ind)
            parent.childs.pop(ind+1)
        if len(parent.keys) == 0:
            parent.cascade()

    def cascade(self):
        parent = self.parent
        if parent is not None:
            for i, otrok in enumerate(parent.childs):
                if otrok == self:
                    if i < len(parent.childs) - 1:
                        self.keys.append(parent.keys[i])
                        zdruzi = parent.childs[i+1]
                        self.keys = self.keys + zdruzi.keys
                        self.childs = self.childs + zdruzi.childs
                        parent.keys.pop(i)
                        parent.childs.pop(i+1)
                        if len(parent.keys) == 0:
                            parent.cascade()
                    else:
                        self.keys.append(parent.keys[i-1])
                        zdruzi = parent.childs[i-1]
                        self.keys = zdruzi.keys + self.keys
                        self.childs = zdruzi.childs + self.childs
                        parent.keys.pop(i-1)
                        parent.childs.pop(i-1)
                        if len(parent.keys) == 0:
                            parent.cascade()
                    break
                        
                        
                    
            
        
            
        
            
                        
                
            
            
