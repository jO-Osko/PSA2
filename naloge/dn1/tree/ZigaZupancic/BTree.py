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
        if self.search(item):
            return None
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
            index = bisect.bisect(node.keys, item)
            self.insert(item, node.children[index])
        if force:
            return left_child, right_child

    def remove(self, item, force=False):
        """
        Odstrani element item iz iskalnega drevesa, če ga ni naj metoda sproži ValueError
        :param item: Element, ki ga brišemo iz drevesa
        :return: None
        """
        if not self.search(item):
            raise ValueError("Item not in tree")
        node = self.root
        while item not in node.keys:
            index = bisect.bisect(node.keys, item)
            node = node.children[index]
        if node.children is None or force:
            if len(node.keys) == self.order and self.root is not node:
                index = bisect.bisect(node.parent.keys, node.keys[0])
                if len(node.parent.keys) > index and len(node.parent.children[index + 1].keys) > self.order:
                    # Rotacija levo
                    right_sibling = node.parent.children[index + 1]
                    node.keys.append(node.parent.keys[index])
                    node.parent.keys[index] = right_sibling.keys[0]
                    right_sibling.keys = right_sibling.keys[1:]
                    node.keys.remove(item)
                elif index > 0 and len(node.parent.children[index - 1].keys) > self.order:
                    # Rotacija desno
                    left_sibling = node.parent.children[index - 1]
                    node.keys.insert(0, node.parent.keys[index])
                    node.parent.keys[index] = left_sibling.keys[-1]
                    left_sibling.keys = left_sibling.keys[:-1]
                    node.keys.remove(item)
                else:
                    # Spoji s sorojencem in vmes postavi ločno vrednost iz straša
                    if index > 0:
                        left = node.parent.children[index - 1]
                        right = node
                    else:
                        left = node
                        right = node.parent.children[index + 1]
                    left.keys.append(node.parent.keys[index - 1])
                    left.keys += right.keys
                    left.keys.remove(item)
                    if force:
                        left.children += right.children
                        for child in right.children:
                            child.parent = left
                    node.parent.children.remove(right)
                    if left.parent.parent is None and len(left.parent.keys) == 1:
                        # Smo v korenu in koren ima le en ključ
                        self.root = left
                        left.parent = None
                    else:
                        self.remove(node.parent.keys[index - 1], force=True)
            else:
                node.keys.remove(item)
        else:
            min_leaf = node.children[bisect.bisect_right(node.keys, item)]
            while min_leaf.children is not None:
                min_leaf = min_leaf.children[0]
            index = bisect.bisect_left(node.keys, item)
            min_element = min_leaf.keys[0]
            self.remove(min_element)
            self.replace(item, min_element)

    def replace(self, item1, item2, node=None):
        """
        Najde element item1, če obstaja ter ga zamenja z item2, če je to možno.
        :param item1: Element, ki ga želimo zamenjati
        :param item2: Element s katerim ga želimo zamenjati
        :param node: Vozišče iz katerega iščemo
        :return: True, če je izmenjava možna in se je izvršila, drugače False.
        """
        if node is None:
            node = self.root
        pos = bisect.bisect(node.keys, item1)
        if pos > 0 and item1 == node.keys[pos - 1]:
            node.keys[pos - 1] = item2
            return True
        elif node.children is not None:
            return self.replace(item1, item2, node.children[pos])
        return False

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
