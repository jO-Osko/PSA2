# -*- coding: utf-8 -*-


"""Time tests"""
import random

from tree.AbstractTree import AbstractTree
from typing import TypeVar, Callable, Optional, Any
from time import process_time

__author__ = "Filip Koprivec"

T = TypeVar("T", bound=AbstractTree)


class AbstractTest:
    short_name = "Test"
    long_name = "Abstract Test"

    def __init__(self, test_size: int, tree: Any, timer: Optional[Callable[..., float]] = None) -> None:
        self.test_size = test_size
        self.tree = tree()  # type: AbstractTree
        if timer is None:
            self.timer = process_time
        else:
            self.timer = timer
        self.data = None  # type: Any

    def prepare(self) -> None:
        raise NotImplementedError("Not implemented")

    def test(self) -> None:
        raise NotImplementedError("Not implemented")

    def time_it(self) -> float:
        self.prepare()
        start_time = self.timer()
        self.test()
        return self.timer() - start_time


class LinearInsert(AbstractTest):
    short_name = "ord ins"
    long_name = "Ordered insert"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)

    def prepare(self) -> None:
        self.data = list(range(self.test_size))


class RandomInsert(AbstractTest):
    short_name = "rand ins"
    long_name = "Randomized insert"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        random.shuffle(self.data)


class InsertAndSearch(AbstractTest):
    short_name = "ord ins sea"
    long_name = "Ordered insert and search"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)
        for j in self.data:
            j in tree

    def prepare(self) -> None:
        self.data = list(range(self.test_size))


class RandomInsertAndSearch(AbstractTest):
    short_name = "rand ins sea"
    long_name = "Random insert and search"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)
        for j in self.data:
            j in tree

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        random.shuffle(self.data)


class OrderedSearchIntensive(AbstractTest):
    short_name = "ord se int"
    long_name = "Ordered search intensive"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)
        for k in range(10):
            for j in self.data:
                j in tree

    def prepare(self) -> None:
        self.data = list(range(self.test_size))


class RandomSearchIntensive(AbstractTest):
    short_name = "rand se int"
    long_name = "Random search intensive"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)
        for k in range(10):
            for j in self.data:
                j in tree

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        random.shuffle(self.data)


class OrderedDeleteDirect(AbstractTest):
    short_name = "ord del dir"
    long_name = "Ordered delete same order"

    def test(self) -> None:
        tree = self.tree
        for j in self.data[0]:
            tree.insert(j)
        for j in self.data[1]:
            tree.remove(j)

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        self.data = self.data, list(self.data)


class OrderedDeleteReverse(AbstractTest):
    short_name = "ord del rev"
    long_name = "Ordered delete reversed order"

    def test(self) -> None:
        tree = self.tree
        for j in self.data[0]:
            tree.insert(j)
        for j in self.data[1]:
            tree.remove(j)

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        self.data = self.data, list(reversed(self.data))


class RandomDelete(AbstractTest):
    short_name = "rand del"
    long_name = "Random delete"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)
        for j in self.data:
            tree.remove(j)

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        random.shuffle(self.data)


class RandomDeleteRandom(AbstractTest):
    short_name = "rand del rand"
    long_name = "Random Random delete"

    def test(self) -> None:
        tree = self.tree
        for j in self.data[0]:
            tree.insert(j)
        for j in self.data[1]:
            tree.remove(j)

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        data2 = list(self.data)
        random.shuffle(data2)
        random.shuffle(self.data)
        self.data = self.data, data2


class SearchSame(AbstractTest):
    short_name = "sea same"
    long_name = "Search the same element"

    def test(self) -> None:
        tree = self.tree
        for j in self.data:
            tree.insert(j)
        zr = self.data[0]
        for j in range(len(self.data)):
            zr in tree

    def prepare(self) -> None:
        self.data = list(range(self.test_size))
        random.shuffle(self.data)
