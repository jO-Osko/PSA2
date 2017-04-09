from ..AbstractTree import AbstractTree
from .Node import Node

__author__ = "Luka Avbreht"


class Avl(AbstractTree):
    """
    Clas that implements Avl tree on top of abstract tree class
    """
    def __init__(self, data=None):
        self.depth = 0
        self.root = None
        if data is not None:
            #self.root = Node(data[0])
            for i in data:
                self.insert(i)
                print(self.depth)
        super().__init__()

    def insert(self, T):
        # So we insert into empty tree
        if self.root is None:
            self.root = Node(T)
            self.depth = 1
        else:
            dodali = False
            # Rebalance is the indicator parameter, that tells us if rebalancig is needet
            # and does the rebalacing of type rebalance[1]
            rebalancingNeedet = False
            subroot = self.root
            while not dodali:
                # We go left
                if T < subroot.value:
                    # We need to go deeper into left tree
                    if subroot.right is not None and subroot.left is not None:
                        subroot = subroot.left
                    # we just add, we dont need to do any rebalancing
                    elif subroot.left is None:
                        subroot.left = Node(value=T, parent=subroot)
                        if self.depth < subroot.left.depth+1:
                            self.depth = 1 + subroot.left.depth
                            rebalancingNeedet = True
                        dodali = True
                    elif subroot.right is None and subroot.left is not None:
                        # We rebalance LL
                        if T < subroot.left.value:
                            self.LLRotation(subroot, T)
                            dodali = True
                        # We rebalance LR
                        else:
                            self.LRRotation(subroot, T)
                            dodali = True
                # We go right
                elif T > subroot.value:
                    # We need to go deeper into right tree
                    if subroot.right is not None and subroot.left is not None:
                        subroot = subroot.right
                    elif subroot.right is None:
                        subroot.right = Node(value=T, parent=subroot)
                        if self.depth < subroot.right.depth+1:
                            self.depth = 1 + subroot.right.depth
                            rebalancingNeedet = True
                        dodali = True
                    elif subroot.right is not None and subroot.left is None:
                        # we rebalance RL
                        if T < subroot.right.value:
                            self.RLRotation(subroot, T)
                            dodali = True
                        # we rebalance RR
                        else:
                            self.RRRotation(subroot, T)
                            dodali = True
                elif T == subroot.value:
                    break
            if rebalancingNeedet:
                self.rebalance(self.root)

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
        while i < self.depth:
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
        pass

    def LLRotation(self,RebalanceNode,addNode = None):
        """
        Does the Left-Left rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree (add node is a value)
        """
        if addNode is not None:
            value1 = RebalanceNode.value
            value2 = RebalanceNode.left.value
            value3 = addNode
            parent = RebalanceNode.parent
            new_node = Node(value=value2, parent=parent)
            new_node.left = Node(value=value3, parent=new_node)
            new_node.right = Node(value=value1, parent=new_node)
        else:
            pass

    def LRRotation(self, RebalanceNode, addNode = None):
        """
        Does the Left-Right rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree ( add node is a value)
        """
        if addNode is not None:
            value1 = RebalanceNode.value
            value2 = RebalanceNode.left.value
            value3 = addNode
            parent = RebalanceNode.parent
            new_node = Node(value=value3, parent=parent)
            new_node.left = Node(value=value2, parent=new_node)
            new_node.right = Node(value=value1, parent=new_node)
        else:
            pass

    def RLRotation(self,RebalanceNode,addNode = None):
        """
        Does the Right-Left rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree ( add node is a value)
        """
        if addNode is not None:
            value1 = RebalanceNode.value
            value2 = RebalanceNode.right.value
            value3 = addNode
            parent = RebalanceNode.parent
            new_node = Node(value=value3, parent=parent)
            new_node.left = Node(value=value1, parent=new_node)
            new_node.right = Node(value=value2, parent=new_node)
        else:
            pass



    def RRRotation(self,RebalanceNode,addNode = None):
        """
        Does the Right-Right rebalancing od Subtree with root node RebalanceNode,
        if addNode is not none, it rotates and adds addNode into tree ( add node is a value)
        """
        if addNode is not None:
            value1 = RebalanceNode.value
            value2 = RebalanceNode.right.value
            value3 = addNode
            parent = RebalanceNode.parent
            new_node = Node(value=value2, parent=parent)
            new_node.left = Node(value=value1, parent=new_node)
            new_node.right = Node(value=value2, parent=new_node)
        else:
            pass

    def __str__(self):
        if self.root is None:
            return "None"
        return str(self.root)

