# -*- coding: utf-8 -*-

"""Generate report"""
from users import get_users

__author__ = "Filip Koprivec"

from tree.AbstractTree import AbstractTree
from typing import TypeVar

from matplotlib import pyplot as pyplot
from matplotlib import patches

T = TypeVar("T", bound=AbstractTree)

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


def main(size: int = 10 ** 4) -> None:
    users = get_users(add_naive=False)

    timings = []

    for test in tests:
        print("Testing:", test.long_name)
        temp_time = []
        timings.append(temp_time)
        for user in users:
            test_instance = test(size, user.tree)  # type: AbstractTest
            print("\t" + user.class_name, end=": ")
            try:
                tested_time = test_instance.time_it()
                temp_time.append(tested_time)
            except (RecursionError, AttributeError, AssertionError):
                temp_time.append(0)
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
