# -*- coding: utf-8 -*-

"""Generate report"""

__author__ = "Filip Koprivec"

import importlib
from tree.AbstractTree import AbstractTree
from typing import Type, TypeVar, List

from matplotlib import pyplot as pyplot
from matplotlib import patches

T = TypeVar("T", bound=AbstractTree)


class UserData:
    def __init__(self, user_name: str, file_name: str, class_name: str, tree: Type[T], color_code: str) -> None:
        self.user_name = user_name
        self.file_name = file_name
        self.class_name = class_name
        self.tree = tree
        self.color_code = color_code

# Za resno testiranje odstranite vzorec, saj je zelo počasen.
trees = [
    ("vzorec", "NaiveTree", "NaiveTree", "r"),
    ("FilipKoprivec", "RedBlackTree", "RedBlackTree", "b"),
]

from time_tests import LinearInsert, AbstractTest, RandomInsert, InsertAndSearch, RandomInsertAndSearch, \
    OrderedSearchIntensive, RandomSearchIntensive, OrderedDeleteDirect, OrderedDeleteReverse, RandomDelete, \
    RandomDeleteRandom, SearchSame

tests = [
    LinearInsert,
    RandomInsert,
    InsertAndSearch,
    RandomInsertAndSearch,
    OrderedSearchIntensive,
    RandomSearchIntensive,
    OrderedDeleteDirect,
    OrderedDeleteReverse,
    RandomDelete,
    RandomDeleteRandom,
    SearchSame,
]


def import_helper(user_name: str, file_name: str, class_name: str, prefix: str = "tree") -> Type[T]:
    tree = getattr(importlib.import_module(".".join([prefix, user_name, file_name])), class_name)
    return tree


def main(size: int = 10 ** 3) -> None:
    users = []  # type: List[UserData]
    for user_name, file_name, class_name, color_code in trees:
        users.append(UserData(user_name, file_name, class_name,
                              import_helper(user_name, file_name, class_name),
                              color_code))

    timings = []

    for test in tests:
        print("Testing:", test.long_name)
        temp_time = []
        timings.append(temp_time)
        for user in users:
            test_instance = test(size, user.tree)  # type: AbstractTest
            print("\t" + user.class_name, end=": ")
            temp_time.append(test_instance.time_it())
            print(temp_time[-1])

    pyplot.figure(figsize=(20, 10))
    pyplot.legend(handles=[patches.Patch(color=user.color_code, label=user.class_name) for user in users])
    for j in range(len(tests)):
        for i in range(len(users)):
            pyplot.plot([j], [timings[j][i]], "o" + users[i].color_code)

    pyplot.xticks(range(len(tests)), [test.short_name.replace(" ", "\n") for test in tests])
    pyplot.title("Prikaz časov za N=" + str(size))
    pyplot.savefig("plot.png")
    pyplot.show()


if __name__ == '__main__':
    main()
