from ..AbstractTree import AbstractTree
from .Node import Node

__author__ = "Luka Avbreht"


class AvlTree(AbstractTree):
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

    def recompute_heights(self, start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.depth
            node.depth = node._depth()
            changed = node.depth != old_height
            node = node.parent

    def left_most(self, root_node):
        """returns the left most node in tree with root root_node """
        node = root_node
        while node.left is not None:
            node = node.left
        return node

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
        while adding_to.parent is not None:
            adding_to._depth()
            adding_to = adding_to.parent
            self.rebalance(adding_to)
        adding_to._depth()

    def remove(self, T):
        """
        Removes item T form Avl tree
        """
        subroot = self.root
        i = 0
        while i < self.root.depth+1:
            if T == subroot.value:
                break
            elif T < subroot.value:
                if subroot.left is not None:
                    subroot = subroot.left
                else:
                    assert ValueError("no such element with value {0}".format(T))
                    break
            else:
                if subroot.right is not None:
                    subroot = subroot.right
                else:
                    assert ValueError("no such element with value {0}".format(T))
                    break
        rotatefrom = None
        parentof = subroot.parent
        if parentof is None:
            camefrom = 0
        elif parentof.right == subroot:
            camefrom = 1
        else:
            camefrom = -1
        if subroot.left is None:
            if subroot.right is None:
                if camefrom == 1:
                    parentof.right = None
                    self.recompute_heights(parentof)
                    rotatefrom = parentof
                elif camefrom == -1:
                    parentof.left = None
                    self.recompute_heights(parentof)
                    rotatefrom = parentof
                elif camefrom == 0:
                    self.root = None
                else:
                    assert ValueError("od nikjer nismo prsli....")
            else:
                if camefrom == 1:
                    parentof.right = subroot.right
                    subroot.right.parent = parentof
                    self.recompute_heights(parentof.right)
                    rotatefrom = parentof.right
                elif camefrom == -1:
                    parentof.left = subroot.right
                    subroot.right.parent = parentof
                    self.recompute_heights(parentof.left)
                    rotatefrom = parentof.left
                elif camefrom == 0:
                    self.root = subroot.right
                    self.root.parent = None
                    self.recompute_heights(self.root)
                    rotatefrom = self.root
                else:
                    assert ValueError("od nikjer nismo prsli....")
        else:
            # left is not None
            if subroot.right is None:
                if camefrom == 0:
                    self.root = subroot.left
                    self.root.parent = None
                    self.recompute_heights(self.root)
                elif camefrom == 1:
                    parentof.right = subroot.left
                    subroot.left.parent = parentof
                    self.recompute_heights(parentof.right)
                elif camefrom == -1:
                    parentof.left = subroot.left
                    subroot.left.parent = parentof
                    self.recompute_heights(parentof.left)
                else:
                    assert ValueError("od nikjer nismo prsli....")
            else:
                najbollev = self.left_most(subroot.right)
                if camefrom == 0:
                    self.root.value = najbollev.value
                elif camefrom == 1 or camefrom == -1:
                    subroot.value = najbollev.value
                else:
                    assert ValueError("od nikjer nismo prsli....")
                if najbollev.parent.left == najbollev:
                    rotatefrom = najbollev.parent
                    if najbollev.right:
                        najbollev.parent.left = najbollev.right
                        najbollev.right.parent = najbollev.parent
                    else:
                        najbollev.parent.left = None
                else:
                    rotatefrom = najbollev.parent
                    if najbollev.right:
                        najbollev.parent.right = najbollev.right
                        najbollev.right.parent = najbollev.parent
                    else:
                        najbollev.parent.right = None
        if rotatefrom is not None:
            while rotatefrom.parent is not None:
                rotatefrom = rotatefrom.parent
                rotatefrom._depth()
                self.rebalance(rotatefrom)
            self.rebalance(rotatefrom)
            rotatefrom._depth()

    def search(self, T):
        """
        Returns True if T is an item of Avl tree
        """
        if self.root is None:
            return False
        subroot = self.root
        i = 0
        while i < self.root.depth+1:
            if T == subroot.value:
                return True
            elif T < subroot.value:
                if subroot.left is not None:
                    subroot = subroot.left
                else:
                    return False
            else:
                if subroot.right is not None:
                    subroot = subroot.right
                else:
                    return False
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


