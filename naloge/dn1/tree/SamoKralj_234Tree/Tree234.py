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
    def __init__(self, value = None):
        self.key = [('V', value)] if value is not None else []
        self.parent = None
        self.depth = 0

    def __repr__(self):
        return str(self.key)
                        
                
            
            
