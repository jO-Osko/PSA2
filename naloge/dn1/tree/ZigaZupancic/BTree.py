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

    def insert(self, item, node=None, force=False):
        """
        Vstavi element item v iskalno drevo, če ta element že obstaja ga prepišemo z novim
        :param item: Element, ki ga vstavljamo v drevo
        :param node: Vozlišče, v katerega vstavljamo element
        :param force: True, če vstavljamo direktno v izbrano vozlišče, tudi če ima otroke, sicer False
        :return: None
        """
        left_child = None
        right_child = None
        if node is None:
            node = self.root
        if node.children is None or force:
            if len(node.keys) == 2*self.order:
                # Ustvari novi vozlišči -- vsako dobi polovico ključev, element na sredini pošlje staršu.
                position = bisect.bisect(node.keys, item)
                if position < self.order:
                    right_child = BTreeNode(node.keys[self.order:], None, node.parent)
                    left_child = BTreeNode(node.keys[:self.order - 1], None, node.parent)
                    bisect.insort(left_child.keys, item)
                    extra_item = node.keys[self.order-1]
                    if node.children is not None:
                        left_child.children = node.children[:self.order]
                        right_child.children = node.children[self.order:]
                elif position > self.order:
                    right_child = BTreeNode(node.keys[self.order+1:], None, node.parent)
                    left_child = BTreeNode(node.keys[:self.order], None, node.parent)
                    bisect.insort(right_child.keys, item)
                    extra_item = node.keys[self.order]
                    if node.children is not None:
                        left_child.children = node.children[:self.order+1]
                        right_child.children = node.children[self.order+1:]
                else:
                    right_child = BTreeNode(node.keys[self.order:], None, node.parent)
                    left_child = BTreeNode(node.keys[:self.order], None, node.parent)
                    extra_item = item
                    if node.children is not None:
                        left_child.children = node.children[:self.order]
                        right_child.children = node.children[self.order-1:]
                if node.parent is not None:
                    if len(node.parent.keys) == 2*self.order:
                        left, right = self.insert(extra_item, node.parent, True)
                        position = bisect.bisect(node.parent.keys, node.keys[0])
                        if position > self.order:
                            right.children.insert(position - self.order, right_child)
                            right.children.insert(position - self.order, left_child)
                            left_child.parent, right_child.parent = right, right
                        elif position < self.order:
                            left.children.insert(position, right_child)
                            left.children.insert(position, left_child)
                            left_child.parent, right_child.parent = left, left
                        else:
                            left.children.append(left_child)
                            right.children.insert(0, right_child)
                            left_child.parent, right_child.parent = left, right
                        if node in left.children:
                            left.children.remove(node)
                        if node in right.children:
                            right.children.remove(node)
                    else:
                        position = bisect.bisect(node.parent.keys, extra_item)
                        node.parent.keys.insert(position, extra_item)
                        node.parent.children.insert(position, left_child)
                        node.parent.children.insert(position + 1, right_child)
                        node.parent.children.remove(node)
                else:
                    self.root = BTreeNode([extra_item], [left_child, right_child])
                    left_child.parent = self.root
                    right_child.parent = self.root
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
        if force:
            return left_child, right_child

    def remove(self, item):
        """
        Odstrani element item iz iskalnega drevesa, če ga ni naj metoda sproži ValueError
        :param item: Element, ki ga brišemo iz drevesa
        :return: None
        """
        raise NotImplementedError("Not implemented")

    def search(self, item, node=None):
        """
        Vrne True, če se item nahaja v drevesu in False, če se ne.
        :param item: Element, ki ga v drevesu iščemo
        :param node: Vozlišče iz katerega iščemo
        :return: True če se item nahaja v drevesu, drugače False.
        """
        if node is None:
            node = self.root
        pos = bisect.bisect(node.keys, item)
        if pos > 0 and item == node.keys[pos - 1]:
            return True
        elif node.children is not None:
            return self.search(item, node.children[pos])
        return False
