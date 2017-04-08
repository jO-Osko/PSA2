# -*- coding: utf-8 -*-
from ..AbstractTree import AbstractTree
from .BTreeNode import BTreeNode
import bisect

__author__ = "Žiga Zupančič"


class BTree(AbstractTree):
    def __init__(self, data, order=1):
        super().__init__(data)
        self.root = BTreeNode()
        self.order = order
        for item in data:
            self.insert(item)

    def __str__(self):
        return str(self.root)
    def __repr__(self):
        return str(self.root)

    def insert(self, item, node=None):
        """
        Vstavi element item v iskalno drevo, če ta element že obstaja ga prepišemo z novim
        :param item: Element, ki ga vstavljamo v drevo
        :param node: Vozlišče, v katerega vstavljamo element
        :return: None
        """
        if node is None:
            node = self.root
        if node.children is None:
            if len(node.keys) == 2*self.order:
                # Ustvari novi vozlišči -- vsako dobi polovico ključev, element na sredini pošlje staršu.
                position = bisect.bisect(node.keys, item)
                if position < self.order:
                    right_child = BTreeNode(node.keys[self.order:])
                    left_child = BTreeNode(node.keys[:self.order - 1])
                    bisect.insort(left_child.keys, item)
                    if node.parent is None:
                        self.root = BTreeNode([node.keys[self.order-1]], [left_child, right_child])
                        left_child.parent = self.root
                        right_child.parent = self.root
                    else:
                        parent_pos = self.send_to_parent(node, node.keys[self.order-1])
                        node.parent.children.insert(parent_pos + 1, right_child)
                elif position > self.order:
                    right_child = BTreeNode(node.keys[self.order+1:])
                    left_child = BTreeNode(node.keys[:self.order])
                    bisect.insort(right_child.keys, item)
                    if node.parent is None:
                        self.root = BTreeNode([node.keys[self.order]], [left_child, right_child])
                        left_child.parent = self.root
                        right_child.parent = self.root
                    else:
                        parent_pos = self.send_to_parent(node, node.keys[self.order])
                        node.parent.children.insert(parent_pos + 1, right_child)
                else:
                    right_child = BTreeNode(node.keys[self.order:])
                    left_child = BTreeNode(node.keys[:self.order])
                    if node.parent is None:
                        self.root = BTreeNode([item], [left_child, right_child])
                        left_child.parent = self.root
                        right_child.parent = self.root
                    else:
                        parent_pos = self.send_to_parent(node, node.keys[item])
                        node.parent.children.insert(parent_pos + 1, right_child)
            else:
                bisect.insort(node.keys, item)
        else:
            # TODO: Izboljsaj iskanje indeksa z bisekcijo
            index = len(node.keys)
            for i, key in enumerate(node.keys):
                if item < key:
                    index = i
                    break
            self.insert(item, node.children[index])

    def send_to_parent(self, node, item):
        if len(node.parent.keys) == 2*self.order:
            raise Warning("Parent node is full!")
        else:
            position = bisect.bisect(node.parent.keys, item)
            node.parent.keys.insert(position, item)
            return position

    def remove(self, item):
        """
        Odstrani element item iz iskalnega drevesa, če ga ni naj metoda sproži ValueError
        :param item: Element, ki ga brišemo iz drevesa
        :return: None
        """
        raise NotImplementedError("Not implemented")

    def search(self, item):
        """
        Vrne True, če se item nahaja v drevesu in False, če se ne.
        :param item: Element, ki ga v drevesu iščemo
        :return: True če se item nahaja v drevesu, drugače False.
        """
        raise NotImplementedError("Not implemented")
