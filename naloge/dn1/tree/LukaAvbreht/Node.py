__author__ = "Luka Avbreht"
import queue


class Node():

    # TODO Probably havinf left and right node in init is kinda stupid, idk

    def __init__(self, value, parent=None):
        """
        Class that creates the structure for Avl to work on (only called once)
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

        self.depth = 0 # to je dejanska globina

    def balance(self):
        return (self.right.depth if self.right else -1) - (self.left.depth if self.left else -1)

    def __str__(self):
        return self.posorder()

    def inorder(self):
        """
        string methot to return a tree in order (left value right)
        """
        if self.left is not None:
            if self.right is not None:
                return " left:(" + str(self.left) + ") " + str(self.value) + "[" + str(self.depth) + "]" + " right:(" + str(self.right) + ")"
            else:
                return " left:(" + str(self.left) + ") " + str(self.value) + "[" + str(self.depth) + "]" + " right:( )"
        else:
            if self.right is not None:
                return " left:(" + " " + ") " + str(self.value) + "[" + str(self.depth) + "]" + " right:(" + str(self.right) + ")"
            else:
                return str(self.value) + "[" + str(self.depth) + "]"

    def posorder(self):
        """
        string methot to return tree in posorder (left right value)
        """
        if self.left is not None:
            if self.right is not None:
                return str(self.value) + "[" + str(self.depth) + "]" + " left:(" + str(self.left) + ")" + " right:(" + str(self.right) + ")"
            else:
                return str(self.value) + "[" + str(self.depth) + "]" + " left:(" + str(self.left) + ")" + " right:(" + " " + ")"
        else:
            if self.right is not None:
                return str(self.value) + "[" + str(self.depth) + "]" + " left:(" + " " + ")" + " right:(" + str(self.right) + ")"
            else:
                return str(self.value) + "[" + str(self.depth) + "]"

    def preorder(self):
        """
        String methot to print tree in preorder (value left right)
        :return:
        """

    def _depth(self):
        if self.left is None:
            lefti  = -1
            if self.right is None:
                righti = -1
            else:
                righti = self.right.depth
        else:
            if self.right is None:
                righti = -1
            else:
                righti = self.right.depth
            lefti = self.left.depth
        self.depth = 1+max(lefti,righti)
        return 1+max(lefti,righti)










