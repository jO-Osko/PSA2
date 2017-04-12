__author__ = "Luka Avbreht"
import queue


class Node():

    # TODO Probably havinf left and right node in init is kinda stupid, idk

    def __init__(self, value, left=None, right=None, parent=None):
        """
        Class that creates the structure for Avl to work on (only called once)
        """
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        if parent != None:
            self.level = parent.level+1
        else:
            self.level = 0

        self.depth = 0 # to je dejanska globina

    def __str__(self):
        if self.left is not None:
            if self.right is not None:
                return str(self.value) + "[" + str(self.level) + "]" + " left:(" + str(self.left) + ")" + " right:(" + str(self.right) + ")"
            else:
                return str(self.value) + "[" + str(self.level) + "]" + " left:(" + str(self.left) + ")" + " right:(" + " " + ")"
        else:
            if self.right is not None:
                return str(self.value) + "[" + str(self.level) + "]" + " left:(" + " " + ")" + " right:(" + str(self.right) + ")"
            else:
                return str(self.value) + "[" + str(self.level) + "]"


    def calculate_depth(self):
        res = 0
        a = queue.Queue()
        a.put(self)
        while not a.empty():
            js = a.get()
            if js.left is not None:
                if js.left.level > res:
                    res = js.left.level
                    a.put(js.left)
            if js.right is not None:
                if js.right.level > res:
                    res = js.right.level
                    a.put(js.right)
        return res+1










