from ..AbstractTree import AbstractTree
from .Node import Node

__author__ = "Luka Avbreht"


class Avl(AbstractTree):
    """
    Clas that implements Avl tree on top of abstract tree class
    """
    def __init__(self, data=None):
        self.root = None
        if data is not None:
            for i in data:
                self.insert(i)
        super().__init__()

    def insert(self, T):
        # So we insert into empty tree
        adding_to = self.root
        if adding_to is None:
            self.root = Node(T)
            self.root.depth = 1
            return
        else:
            while True:
                if T < adding_to.value:
                    if adding_to.left is not None:
                        adding_to = adding_to.left
                    else:
                        adding_to.left = Node(T,parent=adding_to)
                        if adding_to.depth == 0:
                            adding_to.depth = 1
                        adding_to = adding_to.left
                        break
                elif T > adding_to.value:
                    if adding_to.right is not None:
                        adding_to = adding_to.right
                    else:
                        adding_to.right = Node(T,parent=adding_to)
                        if adding_to.depth == 0:
                            adding_to.depth = 1
                        adding_to = adding_to.right
                        break
                else:
                    raise "can only add one element of value"
        print("rebalanciranje")

        while adding_to.parent is not None:
            adding_to._depth()
            adding_to = adding_to.parent
            adding_to = self.rebalance(adding_to)


    def remove(self, T):
        """
        Removes item T form Avl tree
        """
        pass

    def search(self, T):
        """
        Returns True if T is an item of Avl tree
        """
        if self.root is None:
            return False
        subroot = self.root
        i = 0
        while i < self.root.depth:
            if T == subroot.value:
                return True
            elif T < subroot.value:
                subroot = subroot.left
            else:
                subroot = subroot.right
            i += 1
        return False
            # raise NotImplementedError("Not yet done")

    # We always rebalance node with the noode that is in the root
    def rebalance(self, RebalanceNode):
        """
        Rebalances the tree with the root in RebalanceNode, it calls the sub method depending on type of rebalancing required
        """
        if RebalanceNode.balance() < -1:
        # left heawy
            if RebalanceNode.left.balance() < 1:
            # it is not right heawy
                RebalanceNode = self.RRRotation(RebalanceNode)
            else:
            #it is left heawy
                RebalanceNode = self.LRRotation(RebalanceNode)
        elif RebalanceNode.balance() > 1:
            if RebalanceNode.right.balance() > -1:
                RebalanceNode = self.LLRotation(RebalanceNode)
            else:
                RebalanceNode = self.RLRotation(RebalanceNode)
        print(RebalanceNode,"return od rebalance")
        return RebalanceNode
        # else:
        #     if RebalanceNode.parent is not None:
        #         if RebalanceNode.parent.depth == RebalanceNode.depth:
        #             RebalanceNode.parent.depth +=1
        #

    def LLRotation(self,RebalanceNode):
        """
        Does the Left-Left rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree (add node is a value)
        """
        print("delamo LLRot")
        parenttr = RebalanceNode.parent
        root = RebalanceNode
        righty = RebalanceNode.right
        A = RebalanceNode.left
        B = righty.left
        if B is not None:
            B.parent = root
        root.left = A
        root.right = B
        RebalanceNode = righty
        RebalanceNode.left = root
        RebalanceNode.parent = parenttr
        return RebalanceNode


    def LRRotation(self, RebalanceNode, addNode = None):
        """
        Does the Left-Right rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree ( add node is a value)
        """
        print("not implementet LR rotatoion")
        pass

    def RLRotation(self,RebalanceNode,addNode = None):
        """
        Does the Right-Left rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree ( add node is a value)
        """
        print("not implementet RL rotatoion")
        pass



    def RRRotation(self,RebalanceNode):
        """
        Does the Right-Right rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree ( add node is a value)
        """
        print("delamo RRRot")
        parenttr = RebalanceNode.parent
        root = RebalanceNode
        lefti = RebalanceNode.left
        A = lefti.left   # to nerbim
        B = lefti.right
        if B is not None:
            B.parent = root
        C = RebalanceNode.right
        root.left = B
        root.right = C
        lefti.parent = parenttr
        lefti.left = A  # in tega tut ne
        lefti.right = root
        print("kar dobim oz rrrot",lefti)
        return lefti

    def __str__(self):
        if self.root is None:
            return "None"
        return str(self.root)


