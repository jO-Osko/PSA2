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
        while node is not None:
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
        n = self.find(item)
        if n is None:
            return False
        else:
            self.splay(n)
            return True

    def find(self, item):
        node = self.root
        while node is not None:
            if node.key == item:
                return node
            elif node.key > item:
                node = node.left
            else:
                node = node.right
        return None

    def findMax(self, start=None):
        if start is None:
            start = self.root
        if start is None:
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
        gg = g.parent
        if gg is not None:
            if gg.left == g:
                gg.left = node
            else:
                gg.right = node
        node.parent = gg
        if left:
            l = node.left
            if l:
                l.parent = p
            if p.left:
                p.left.parent = g
            g.right = p.left
            p.right = l
            p.left = g
            g.parent = p
            p.parent = node
            node.left = p
        else:
            r = node.right
            if r:
                r.parent = p
            if p.right:
                p.right.parent = g
            g.left = p.right
            p.left = r
            p.right = g
            g.parent = p
            p.parent = node
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
            if g.parent is not None:
                if g.parent.right is g:
                    g.parent.right = node
                else:
                    g.parent.left = node
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
            if g.parent is not None:
                if g.parent.right is g:
                    g.parent.right = node
                else:
                    g.parent.left = node
            g.parent = node
            p.parent = node
            g.right = l
            p.left = r
            node.right = p
            node.left = g

    def splay(self, node):
        if node is None:
            return
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
            if node.left is not None:
                node.left.parent = None
                m = self.findMax()
                self.splay(m)
                self.root.right = right
                if self.root.right is not None:
                    self.root.right.parent = self.root
            else:
                self.root = right
                if self.root is not None:
                    self.root.parent = None