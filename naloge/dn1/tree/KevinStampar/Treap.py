# -*- coding: utf-8 -*-
import random

__author__ = "Kevin Stampar"


#veja
class Node():
    def __init__(self, key=None, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        self.priority = random.random()

    
    def fixHeap(self):
        #popravi prioritete, ki se pokvarijo ob insertu
        if self.parent != None:
            while self.parent.priority < self.priority:
                if self.parent.right == self:
                    self.lRot()
                elif self.parent.left == self:
                    self.rRot()
                if self.parent == None:
                    break

    def fixHeap2(self):
        #popravi prioritete, ki se pokvarijo ob izbrisu elementa
        if self.left == None and self.right == None:
            pass
        elif self.left == None:
            if self.right.priority > self.priority:
                self.right.fixHeap()
                self.fixHeap2()
        elif self.right == None:
            if self.left.priority > self.priority:
                self.left.fixHeap()
                self.fixHeap2()
        else:
            if self.left.priority > self.right.priority:
                if self.left.priority > self.priority:
                    self.left.fixHeap()
                    self.fixHeap2()
            else:
                if self.right.priority > self.priority:
                    self.right.fixHeap()
                    self.fixHeap2()

    def size(self):
        if self.left != None:
            if self.right != None:
                return 1 + self.left.size() + self.right.size()
            else:
                return 1 + self.left.size()
        elif self.right != None:
            return 1 + self.right.size()
        else:
            return 1

    def insert(self, t):

        #Vstavi element item v iskalno drevo

        if t == self.key:
            self.key = t
            self.priority = random.random()

        elif t < self.key:
            if self.left == None:
                self.left = Node(t, None, None, self)
                self.left.fixHeap()
            else:
                self.left.insert(t)
        else:
            if self.right == None:
                self.right = Node(t, None, None, self)
                self.right.fixHeap()
            else:
                self.right.insert(t)

    def lRot(self):
        #naredi levo rotacijo
        levi = self.left
        noviocka = self.parent.parent
        ocka = self.parent


        self.left = ocka
        ocka.parent = self
        self.parent = noviocka
        self.left.right = levi
        if levi != None:
            levi.parent = self.left
        if self.parent != None:
            if self.parent.left == self.left:
                self.parent.left = self
            elif self.parent.right == self.left:
                self.parent.right = self

    def rRot(self):
        #naredi desno rotacijo
        desni = self.right
        noviocka = self.parent.parent
        ocka = self.parent

        self.right = ocka
        ocka.parent = self
        self.parent = noviocka
        self.right.left = desni
        if desni != None:
            desni.parent = self.right
        if self.parent != None:
            if self.parent.left == self.right:
                self.parent.left = self
            elif self.parent.right == self.right:
                self.parent.right = self

    def remove(self, item):
        #izbrise element iz drevesa
        if item < self.key:
            self.left.remove(item)
        elif item > self.key:
            self.right.remove(item)
        else:
            if self.left == None:
                if self.right == None:
                    if self.parent.left == self:
                        self.parent.left = None
                    else:
                        self.parent.right = None

                else:
                    ocka = self.parent
                    if ocka != None:
                        if ocka.left == self:
                            ocka.left = self.right
                        elif ocka.right == self:
                            ocka.right = self.right
                        self.right.parent = ocka
                        self.right.fixHeap2()

                    else:
                        desni=self.right
                        self.key=desni.key
                        self.left = desni.left
                        self.right = desni.right
                        self.priority = desni.priority
                        self.fixHeap2()



            else:
                if self.right == None:
                    ocka = self.parent
                    if ocka != None:
                        if ocka.left == self:
                            ocka.left=self.left


                        else:
                            ocka.right = self.left
                        self.left.parent = ocka
                        self.left.fixHeap2()

                    else:
                        levi = self.left
                        self.left = levi.left
                        self.right = levi.right
                        self.priority = levi.priority
                        self.key = levi.key
                        self.fixHeap2()


                else:
                    successor = self.successor()
                    self.key = successor.key
                    self.priority = successor.priority
                    successor.parent.left = successor.right
                    if successor.right != None:
                        successor.right.parent = successor.parent
                    self.fixHeap2()






    def search(self, t):
        #pove, ce element je v drevesu ali ne
        if self.key == t:
            return True
        if t < self.key:
            if self.left == None:
                return False
            else:
                return self.left.search(t)
        if t > self.key:
            if self.right == None:
                return False
            else:
                return self.right.search(t)

    def __contains__(self, t):
        return self.search(t)

    def successor(self):
        #vrne naslednika
        if self.left == None:
            return self
        else:
            return self.left.successor()

    def depth(self):
        #vrne globino
        if self.left == None and self.right == None:
            return 0
        elif self.left == None:
            return 1 + self.right.depth()
        elif self.right == None:
            return 1 + self.left.depth()
        else:
            return 1 + max(self.right.depth(), self.left.depth())
#Drevo
class Treap():
    def __init__(self, seznam=None):
        self.root = None
        if seznam != None:
            for i in seznam:
                self.insert(i)

    def fixRoot(self):
        #popravi koren
        if self.root.parent != None:
            self.root = self.root.parent
            self.fixRoot()

    def insert(self, key):
        if self.root == None:
            self.root = Node(key)
        else:
            self.root.insert(key)
            self.fixRoot()



    def depth(self):
        if self.root != None:
            return self.root.depth()
        else:
            return 0

    def search(self, key):
        if self.root == None:
            return False
        else:
            return self.root.search(key)

    def remove(self, key):
        if key not in self:
            raise KeyError("Key not found.")
        elif self.root.key == key:
            if self.root.left == None and self.root.right == None:
                self.root == None
            elif self.root.left == None:
                self.root = self.root.right
                self.root.parent = None
            elif self.root.right == None:
                self.root = self.root.left
                self.root.parent = None

        else: 
            self.root.remove(key)
            self.fixRoot()


    def __contains__(self, t):
        return self.search(t)

    def size(self):
        if self.root != None:
            return self.root.size()
        else:
            return 0


