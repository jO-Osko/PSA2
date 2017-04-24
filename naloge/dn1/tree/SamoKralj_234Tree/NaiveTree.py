# -*- coding: utf-8 -*-
from typing import TypeVar, Iterable, Optional

from ..AbstractTree import AbstractTree

__author__ = "Filip Koprivec"

T = TypeVar("T")


class NaiveTree(AbstractTree):
    def __init__(self, data: Optional[Iterable[T]] = None) -> None:
        self.data = list(data) if data else []
        super().__init__(data)

    def insert(self, item: T) -> None:
        for i, val in enumerate(self.data):
            if val == item:
                self.data[i] = item
                return
        self.data.append(item)

    def search(self, item: T) -> bool:
        for val in self.data:
            if val == item:
                return True
        return False

    def remove(self, item: T) -> None:
        for i, val in enumerate(self.data):
            if val == item:
                del self.data[i]
                return
        raise ValueError("Item not present")
