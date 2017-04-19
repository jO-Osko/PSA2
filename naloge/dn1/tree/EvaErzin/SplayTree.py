# -*- coding: utf-8 -*-


from ..AbstractTree import AbstractTree

__author__ = "Eva Erzin"



class Node:

    def __init__(self, key = None, parent = None, left = None, right = None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        if self.key is None:
            return 'Null'
        else:
            return '{key} ((Left: {left}) (Right: {right}))'.format(key=self.key, left=self.left, right=self.right)

class SplayTree(AbstractTree):

    def __init__(self, data = None):
        self.root = None
        if data:
            for i in data:
                self.insert(i)
        super().__init__()

    def __repr__(self):
        return str(self.root)

    def insert(self, item):
        parent = None
        side = 0 ## 0 if item is left child of parent, else 1
        node = self.root
        while node:
            if item > node.key:
                parent = node
                side = 1
                node = node.right
            elif item < node.key:
                parent = node
                side = 0
                node = node.left
            else:
                return
        node = Node(key=item, parent=parent)
        if not parent:
            self.root = node
        elif side:
            parent.right = node
        else:
            parent.left = node
        self.splay(node)

    def search(self, item):
        node = self.root
        while node:
            if item > node.key:
                node = node.right
            elif item < node.key:
                node = node.left
            else:
                self.splay(node)
                return True
        return False

    def find(self, item):
        node = self.root
        while node:
            if item > node.key:
                node = node.right
            elif item < node.key:
                node = node.left
            else:
                return node
        return None

    def findMax(self, start=None):
        if not start:
            start = self.root
        if not start:
            return
        else:
            while start.right:
                start = start.right
            return start

    def leftRotate(self, node):
        p = node.parent
        g = p.parent
        l = node.left
        p.right = l
        if l:
            l.parent = p
        p.parent = node
        node.left = p
        node.parent = g


    def rightRotate(self, node):
        p = node.parent
        g = p.parent
        r = node.right
        p.left = r
        if r:
            r.parent = p
        p.parent = node
        node.right = p
        node.parent = g

    def zigZig(self, node, left):
        p = node.parent
        g = p.parent
        if left:
            l = node.left
            if l:
                l.parent = p
            if p.left:
                p.left.parent = g
            node.parent = g.parent
            if node.parent:
                if node.parent.left is g:
                    node.parent.left = node
                else:
                    node.parent.right = node
            g.parent = p
            p.parent = node
            g.right = p.left
            p.left = g
            p.right = l
            node.left = p
        else:
            r = node.right
            if r:
                r.parent = p
            if p.right:
                p.right.parent = g
            node.parent = g.parent
            if node.parent:
                if node.parent.left is g:
                    node.parent.left = node
                else:
                    node.parent.right = node
            g.parent = p
            p.parent = node
            g.left = p.right
            p.right = g
            p.left = r
            node.right = p



    def zigZag(self, node, lr):
        p = node.parent
        g = p.parent
        l = node.left
        r = node.right
        if lr:
            if l:
                l.parent = p
            if r:
                r.parent = g
            node.parent = g.parent
            g.parent = node
            p.parent = node
            g.left = node.right
            p.right = node.left
            node.left = p
            node.right = g
        else:
            if l:
                l.parent = g
            if r:
                r.parent = p
            node.parent = g.parent
            g.parent = node
            p.parent = node
            g.right = l
            p.left = r
            node.right = p
            node.left = g

    def splay(self, node):
        while node.parent:
            if not node:
                raise ValueError("This shouldn't have happened")
            elif not node.parent.parent:
                if node.parent.left is node:
                    self.rightRotate(node)
                else:
                    self.leftRotate(node)
            else:
                lc = node.parent.left is node
                lp = node.parent.parent.left is node.parent
                if lc and not lp:
                    self.zigZag(node, 0)
                elif lp and not lc:
                    self.zigZag(node, 1)
                elif lc and lp:
                    self.zigZig(node, 0)
                elif not lp and not lc:
                    self.zigZig(node, 1)
        self.root = node


    def remove(self, item):
        node = self.find(item)
        if not node:
            raise ValueError('The item you are trying to remove does not exist')
        else:
            self.splay(node)
            right = node.right
            self.root = node.left
            node.left.parent = None
            m = self.findMax()
            self.splay(m)
            m.right = right