# -*- coding: utf-8 -*-
from enum import Enum
from typing import TypeVar, Iterable, Optional, Generic, Union, Iterator

from ..AbstractTree import AbstractSearchTree

__author__ = "Filip Koprivec"

T = TypeVar("T")


class Color(Enum):
    RED = 0
    BLACK = 1


GeneralNode = Union["RBNode[T]", "RBNode.SentinelNil"]


class RBNode(Generic[T]):
    __slots__ = ("key", "color", "left_child", "right_child", "parent")

    def __init__(self, key: T, color: Color = Color.BLACK, left_child: GeneralNode = None,
                 right_child: GeneralNode = None, parent: GeneralNode = None) -> None:
        self.key = key
        self.color = color
        self.left_child = left_child or RBNode.NIL
        self.right_child = right_child or RBNode.NIL
        self.parent = parent or RBNode.NIL

    def __repr__(self) -> str:
        return "Node(key={key}, color={color}, left={left}, right={right})".format(key=self.key, color=self.color,
                                                                                   left=self.left_child,
                                                                                   right=self.right_child)

    class SentinelNil(Enum):
        NIL = 0

        def __init__(self, value: int) -> None:
            self.color = Color.BLACK
            self.parent = self  # type: GeneralNode

        def __repr__(self) -> str:
            return "NIL"

    NIL = SentinelNil.NIL


Node = RBNode[T]


class RedBlackTree(AbstractSearchTree, Generic[T]):
    __slots__ = ("root", "data", "_size")

    def __init__(self, data: Optional[Iterable[T]] = None) -> None:
        super().__init__(data)
        self.root = RBNode.NIL  # type: GeneralNode[T]
        self._size = 0
        if data:
            for j in data:
                self.insert(j)

    def insert(self, item: T) -> None:
        z = RBNode(item)
        self.rb_insert(z)

    def rb_insert(self, z: Node) -> None:
        y = RBNode.NIL  # type: GeneralNode
        x = self.root
        while x is not RBNode.NIL:
            assert isinstance(x, RBNode)
            y = x
            if z.key < x.key:
                x = x.left_child
            elif z.key > x.key:
                x = x.right_child
            else:  # z.key == x.key  # Replace
                z.parent = x.parent
                z.left_child = x.left_child
                if z.left_child is not RBNode.NIL:
                    assert isinstance(z.left_child, RBNode)
                    z.left_child.parent = z
                z.right_child = x.right_child
                if z.right_child is not RBNode.NIL:
                    assert isinstance(z.right_child, RBNode)
                    z.right_child.parent = z
                return
        z.parent = y
        if y is RBNode.NIL:  # create first entry
            self.root = z
        else:
            assert isinstance(y, RBNode)  # For mypy
            if z.key < y.key:
                y.left_child = z
            else:
                y.right_child = z
        z.left_child = RBNode.NIL
        z.right_child = RBNode.NIL
        z.color = Color.RED
        self.insert_fixup(z)
        self._size += 1

    def search(self, item: T, root: Optional[GeneralNode] = None) -> bool:
        node = self.find(item, root)
        return node is not RBNode.NIL

    def remove(self, item: T) -> None:
        z = self.find(item)
        if z is RBNode.NIL:
            raise ValueError("Item not present")
        assert isinstance(z, RBNode)
        y = z
        original_color = y.color
        if z.left_child is RBNode.NIL:
            # assert isinstance(z.right_child, RBNode)
            x = z.right_child  # type: GeneralNode
            self.transplant(z, z.right_child)
        elif z.right_child is RBNode.NIL:
            assert isinstance(z.left_child, RBNode)
            x = z.left_child
            self.transplant(z, z.left_child)
        else:
            y = self.get_min_node(z.right_child)
            original_color = y.color
            # assert isinstance(y.right_child, RBNode)
            x = y.right_child
            if y.parent is z:
                # We need it for delete fixup
                x.parent = y
            else:
                # assert isinstance(y.right_child, RBNode)
                self.transplant(y, y.right_child)
                assert isinstance(z.right_child, RBNode)
                y.right_child = z.right_child
                y.right_child.parent = y
            self.transplant(z, y)
            assert isinstance(z.left_child, RBNode)
            y.left_child = z.left_child
            y.left_child.parent = y
            y.color = z.color
        self._size -= 1
        if original_color is Color.BLACK:
            # assert isinstance(x, RBNode)
            self.delete_fixup(x)

    def find(self, item: T, root: Optional[GeneralNode] = None) -> GeneralNode:
        if root is None:
            root = self.root
        if root is RBNode.NIL:  # Empty (sub)tree
            return RBNode.NIL
        cur_root = root
        while cur_root is not RBNode.NIL:
            assert isinstance(cur_root, RBNode)
            if item < cur_root.key:
                cur_root = cur_root.left_child
            elif item > cur_root.key:
                cur_root = cur_root.right_child
            else:  # item == cur_root.key:
                return cur_root
        # Not found
        return RBNode.NIL

    # Mypy problems
    def get_min_node(self, root: Optional[GeneralNode] = None) -> Node:
        if root is None:
            root = self.root
        if self.root is RBNode.NIL:
            raise IndexError("Empty tree")

        assert isinstance(root, RBNode)
        prev = root
        root = root.left_child
        while root is not RBNode.NIL:
            assert isinstance(root, RBNode)
            prev = root
            root = root.left_child
        return prev

    def get_min(self, root: Optional[GeneralNode] = None) -> T:
        return self.get_min_node(root).key

    def get_max_node(self, root: Optional[GeneralNode] = None) -> Node:
        if root is None:
            root = self.root
        if self.root is RBNode.NIL:
            raise IndexError("Empty tree")
        assert isinstance(root, RBNode)
        prev = root
        root = root.right_child
        while root is not RBNode.NIL:
            assert isinstance(root, RBNode)
            prev = root
            root = root.right_child
        return prev

    def get_max(self, root: Optional[GeneralNode] = None) -> T:
        return self.get_max_node(root).key

    def rotate_left(self, x: Node) -> None:
        y = x.right_child
        assert isinstance(y, RBNode)
        x.right_child = y.left_child
        if y.left_child is not RBNode.NIL:
            assert isinstance(y.left_child, RBNode)
            y.left_child.parent = x
        y.parent = x.parent
        if x.parent is RBNode.NIL:
            self.root = y
        else:  # mypy does not yet support this, see https://github.com/python/mypy/issues/1803
            assert isinstance(x.parent, RBNode)
            if x == x.parent.left_child:
                x.parent.left_child = y
            else:
                x.parent.right_child = y
        y.left_child = x
        x.parent = y

    def rotate_right(self, y: Node) -> None:
        x = y.left_child
        assert isinstance(x, RBNode)
        y.left_child = x.right_child
        if x.right_child is not RBNode.NIL:
            assert isinstance(x.right_child, RBNode)
            x.right_child.parent = y
        x.parent = y.parent
        if y.parent is RBNode.NIL:
            self.root = x
        else:  # Same problem as in rotate_right
            assert isinstance(y.parent, RBNode)
            if y == y.parent.right_child:
                y.parent.right_child = x
            else:
                y.parent.left_child = x
        x.right_child = y
        y.parent = x

    def insert_fixup(self, z: Node) -> None:
        while z.parent.color == Color.RED:
            assert isinstance(z.parent, RBNode)
            assert isinstance(z.parent.parent, RBNode)
            if z.parent == z.parent.parent.left_child:
                y = z.parent.parent.right_child
                # assert isinstance(y, RBNode)
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    assert isinstance(z.parent, RBNode)  # mypy problem
                    if z == z.parent.right_child:
                        z = z.parent
                        self.rotate_left(z)
                    assert isinstance(z.parent, RBNode)
                    assert isinstance(z.parent.parent, RBNode)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.rotate_right(z.parent.parent)
            else:
                assert isinstance(z.parent, RBNode)
                assert isinstance(z.parent.parent, RBNode)
                y = z.parent.parent.left_child
                # assert isinstance(y, RBNode)
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    assert isinstance(z.parent, RBNode)  # mypy problem
                    if z == z.parent.left_child:
                        z = z.parent
                        self.rotate_right(z)
                    assert isinstance(z.parent, RBNode)
                    assert isinstance(z.parent.parent, RBNode)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.rotate_left(z.parent.parent)
        assert isinstance(self.root, RBNode)
        self.root.color = Color.BLACK

    def transplant(self, u: GeneralNode, v: GeneralNode) -> None:
        if u.parent is RBNode.NIL:
            self.root = v
        else:
            assert isinstance(u.parent, RBNode)
            if u is u.parent.left_child:
                u.parent.left_child = v
            else:
                u.parent.right_child = v
        v.parent = u.parent

    def delete_fixup(self, x: GeneralNode) -> None:
        while x != self.root and x.color is Color.BLACK:
            assert isinstance(x.parent, RBNode)
            if x is x.parent.left_child:
                w = x.parent.right_child
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.rotate_left(x.parent)
                    w = x.parent.right_child
                assert isinstance(w, RBNode)
                if w.left_child.color is Color.BLACK and w.right_child.color is Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right_child.color is Color.BLACK:
                        w.left_child.color = Color.BLACK
                        w.color = Color.RED
                        self.rotate_right(w)
                        assert isinstance(x.parent, RBNode)
                        w = x.parent.right_child
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    assert isinstance(w, RBNode)
                    w.right_child.color = Color.BLACK
                    assert isinstance(self.root, RBNode)
                    assert isinstance(x.parent, RBNode)
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                assert isinstance(x.parent, RBNode)
                w = x.parent.left_child
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.rotate_right(x.parent)
                    w = x.parent.left_child
                assert isinstance(w, RBNode)
                if w.right_child.color is Color.BLACK and w.left_child.color is Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left_child.color is Color.BLACK:
                        w.right_child.color = Color.BLACK
                        w.color = Color.RED
                        self.rotate_left(w)
                        assert isinstance(x.parent, RBNode)
                        w = x.parent.left_child
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    assert isinstance(w, RBNode)
                    w.left_child.color = Color.BLACK
                    assert isinstance(self.root, RBNode)
                    assert isinstance(x.parent, RBNode)
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def size(self) -> int:
        return self._size

    def in_order_traversal(self, root: Optional[GeneralNode] = None) -> Iterator[T]:
        if root is None:
            root = self.root
        if root is RBNode.NIL:
            return
        assert isinstance(root, RBNode)
        for j in self.in_order_traversal(root.left_child):
            yield j
        yield root.key
        for j in self.in_order_traversal(root.right_child):
            yield j

    def __repr__(self) -> str:
        return "Tree({data})".format(data=repr(self.root))

    def successor(self, x: Node) -> GeneralNode:
        if x.right_child is not RBNode.NIL:
            return self.get_min_node(x.right_child)
        while x.parent is not RBNode.NIL and x is x.parent.right_child:
            x = x.parent
        return x.parent

    def predecessor(self, x: Node) -> GeneralNode:
        if x.left_child is not RBNode.NIL:
            return self.get_max_node(x.left_child)
        while x.parent is not RBNode.NIL and x is x.parent.left_child:
            x = x.parent
        return x.parent
