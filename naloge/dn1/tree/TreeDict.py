# -*- coding: utf-8 -*-


"""Simple dict implementation using AbstractTree"""
from tree.AbstractTree import AbstractSearchTree
from typing import Generic, TypeVar, MutableMapping, Iterator, Optional, Tuple, Any, Callable, List

K_T = TypeVar("K_T")
V_T = TypeVar("V_T")


class DictItem(Generic[K_T, V_T]):
    def __init__(self, key: K_T, value: Optional[V_T]) -> None:
        self.key = key
        self.value = value

    def __lt__(self, other: "DictItem") -> bool:
        return self.key < other.key


AbstractTreeConstructor = Callable[..., AbstractSearchTree[DictItem[K_T, V_T]]]


class SimpleDict(MutableMapping, Generic[K_T, V_T]):
    def __init__(self, base_structure: AbstractTreeConstructor) -> None:
        self.tree = base_structure()

    def __delitem__(self, v: K_T) -> None:
        self.tree.remove(DictItem(v, None))

    def __len__(self) -> int:
        return self.tree.size()

    def __setitem__(self, k: K_T, v: V_T) -> None:
        self.tree.insert(DictItem(k, v))

    def __iter__(self) -> Iterator[K_T]:
        for item in self.tree.in_order_traversal():
            yield item.key

    def __getitem__(self, k: K_T) -> V_T:
        # Mypy complains
        return self.tree.find(DictItem(k, None)).value
