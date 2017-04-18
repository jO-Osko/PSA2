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

    def height(self):
        """
        Depth of tree (max depth)
        """
        if self.root:
            return self.root.depth
        else:
            return 0

    # @staticmethod
    def recompute_heights(self, start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.depth
            node.depth = node._depth()
            changed = node.depth != old_height
            node = node.parent

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
                    raise ValueError("can only add one element of value")
        print("rebalanciranje")

        while adding_to.parent is not None:
            adding_to._depth()
            adding_to = adding_to.parent
            self.rebalance(adding_to)
        adding_to._depth()


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

    def rebalance(self, RebalanceNode):
        """
        Rebalances the tree with the root in RebalanceNode, it calls the sub method depending on type of rebalancing required
        """
        if RebalanceNode.balance() < -1:  # uresnici je -2
            # left heavy
            if RebalanceNode.left.balance() < 1:
                # it is not right heavy
                self.RRRotation(RebalanceNode)
            else:
                # it is left heavy
                self.LRRotation(RebalanceNode)
        elif RebalanceNode.balance() > 1:  # uresici 2
            if RebalanceNode.right.balance() > -1:  # da je njegov desn 0 al pa 1
                self.LLRotation(RebalanceNode)
            else:
                self.RLRotation(RebalanceNode)

    def LLRotation(self, A):
        """
        Does the Left-Left rebalancing od Subtree with root node RebalanceNode,
        """
        print("delamo LLRot")
        parenttt = A.parent
        B = A.right
        C = B.right
        assert (A is not None and B is not None and C is not None)
        A.right = B.left
        if A.right:
            A.right.parent = A
        B.left = A
        A.parent = B
        if parenttt is None:
            # We are at the root
            self.root = B
            self.root.parent = None
        else:
            if parenttt.left == A:
                parenttt.left = B
            else:
                parenttt.right = B
            B.parent = parenttt
        self.recompute_heights(A)
        self.recompute_heights(B.parent)

    def LRRotation(self, A):
        """
        Does the Left-Right rebalancing od Subtree with root node RebalanceNode,
        """
        print("LR rotatoion")
        parenttt = A.parent
        B = A.left
        C = B.right
        assert (A is not None and B is not None and C is not None)
        A.left = C.right
        if A.left:
            A.left.parent = A
        B.right = C.left
        if B.right:
            B.right.parent = B
        C.left = B
        C.right = A
        A.parent = C
        B.parent = C
        if parenttt is None:
            self.root = C
        else:
            if parenttt.left == A:
                parenttt.left = C
            else:
                parenttt.right = C
        C.parent = parenttt
        self.recompute_heights(A)
        self.recompute_heights(B)

    def RLRotation(self, A):
        """
        Does the Right-Left rebalancing od Subtree with root node RebalanceNode,
        """
        print("RL rotatoion")
        parenttt = A.parent
        B = A.right
        C = B.left
        assert (A is not None and B is not None and C is not None)
        A.right = C.left
        if A.right:
            A.right.parent = A
        B.left = C.right
        if B.left:
            B.left.parent = B
        C.right = B
        C.left = A
        A.parent = C
        B.parent = C
        if parenttt is None:
            self.root = C
        else:
            if parenttt.left == A:
                parenttt.left = C
            else:
                parenttt.right = C
        C.parent = parenttt
        self.recompute_heights(A)
        self.recompute_heights(B)

    def RRRotation(self, A):
        """
        Does the Right-Right rebalancing od Subtree with root node RebalanceNode,
        """
        print("delamo RRRot")
        parenttt = A.parent
        B = A.left
        C = B.left
        assert (A is not None and B is not None and C is not None)
        A.left = B.right
        if A.left:
            A.left.parent = A
        B.right = A
        A.parent = B
        if parenttt is None:
            # We are at the root
            self.root = B
            self.root.parent = None
        else:
            if parenttt.right == A:
                parenttt.right = B
            else:
                parenttt.left = B
            B.parent = parenttt
        self.recompute_heights(A)
        self.recompute_heights(B.parent)

    def __str__(self):
        if self.root is None:
            return "None"
        return str(self.root)


