# -*- coding: utf-8 -*-
from ..AbstractTree import AbstractTree
from .BTreeNode import BTreeNode
import bisect

__author__ = "Žiga Zupančič"


class BTree(AbstractTree):
    def __init__(self, data=None, order=1):
        if data is None:
            data = []
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

        if node is None and self.search(item):
            return None
        if len(self.root.keys) == 0:
            self.root.keys.append(item)
            return None
        if node is None:
            node = self.root
        if node.children is None:
            if len(node.keys) == 2*self.order:
                self.split(node, item)
            else:
                bisect.insort(node.keys, item)
        else:
            pos = bisect.bisect(node.keys, item)
            self.insert(item, node.children[pos])

    def split(self, node, item, left=None, right=None, prev_node=None):
        bisect.insort(node.keys, item)
        left_node = BTreeNode(node.keys[:self.order])
        right_node = BTreeNode(node.keys[self.order + 1:])
        extra_item = node.keys[self.order]
        if left is not None and right is not None and prev_node is not None:
            node_keys = [i for i in node.keys if i != item]
            if item > node_keys[self.order]:
                # item je v right_node
                left_node.children = node.children[:len(left_node.keys)+1]
                right_node.children = node.children[len(right_node.keys)+1:]
                pos = right_node.children.index(prev_node)
                right_node.children.insert(pos, right)
                right_node.children.insert(pos, left)
                right_node.children.remove(prev_node)
                right.parent = right_node
                left.parent = right_node
            elif item < node_keys[self.order - 1]:
                # item je v left_node
                left_node.children = node.children[:len(left_node.keys)]
                right_node.children = node.children[len(right_node.keys):]
                pos = left_node.children.index(prev_node)
                left_node.children.insert(pos, right)
                left_node.children.insert(pos, left)
                left_node.children.remove(prev_node)
                right.parent = left_node
                left.parent = left_node
            else:
                # item je extra_item
                left_node.children = node.children[:len(left_node.keys)]
                right_node.children = node.children[len(right_node.keys)+1:]
                right_node.children.insert(0, right)
                left_node.children.append(left)
                right.parent = right_node
                left.parent = left_node
            for child in left_node.children:
                child.parent = left_node
            for child in right_node.children:
                child.parent = right_node
        if node.parent is not None:
            if len(node.parent.keys) == 2*self.order:
                self.split(node.parent, extra_item, left_node, right_node, node)
            else:
                pos = bisect.bisect(node.parent.keys, extra_item)
                node.parent.keys.insert(pos, extra_item)
                node.parent.children.insert(pos, right_node)
                node.parent.children.insert(pos, left_node)
                node.parent.children.remove(node)
                left_node.parent = node.parent
                right_node.parent = node.parent
        else:
            self.root = BTreeNode([extra_item], [left_node, right_node])
            left_node.parent = self.root
            right_node.parent = self.root

    def remove(self, item, force=False):
        """
        Odstrani element item iz iskalnega drevesa, če ga ni naj metoda sproži ValueError
        :param item: Element, ki ga brišemo iz drevesa
        :param force: True, če na silo brišemo iz vozlišča, ki ni otrok
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
                    if force:
                        child = right_sibling.children[0]
                        node.children.append(child)
                        right_sibling.children.remove(child)
                        child.parent = node
                elif index > 0 and len(node.parent.children[index - 1].keys) > self.order:
                    # Rotacija desno
                    left_sibling = node.parent.children[index - 1]
                    node.keys.insert(0, node.parent.keys[index-1])
                    node.parent.keys[index - 1] = left_sibling.keys[-1]
                    left_sibling.keys = left_sibling.keys[:-1]
                    node.keys.remove(item)
                    if force:
                        child = left_sibling.children[-1]
                        node.children.insert(0, child)
                        left_sibling.children.remove(child)
                        child.parent = node
                else:
                    # Spoji s sorojencem in vmes postavi ločno vrednost iz straša
                    if index > 0:
                        left = node.parent.children[index - 1]
                        right = node
                    else:
                        left = node
                        right = node.parent.children[index + 1]
                        index += 1
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
