# -*- coding: utf-8 -*-
from tree.AbstractTree import AbstractTree
from tree.CountingNode import CountingNode
from tree.vzorec.NaiveTree import NaiveTree

from time import process_time
import random


def test_adding(tree: AbstractTree, n: int = 10 ** 4, shuffle: bool = True) -> None:
    ran = list(range(n))
    if shuffle:
        random.shuffle(ran)

    tree.insert(-1)
    for j in ran:
        tree.insert(j)
    tree.insert(-1)
    tree.insert(-1)
    for j in ran:
        assert j in tree
    assert -1 in tree
    # print(list(tree.in_order_traversal()))
    for j in ran:
        tree.remove(j)
    for j in ran:
        assert j not in tree
    tree.remove(-1)
    assert -1 not in tree


def count_adding(tree: AbstractTree, n: int = 10 ** 4, shuffle: bool = True) -> None:
    ran = list(range(n))

    if shuffle:
        random.shuffle(ran)

    c_node = CountingNode()
    items = [c_node.create_new_node(j) for j in ran]

    m1 = c_node.create_new_node(-1)

    tree.insert(m1)
    tree.insert(m1)
    tree.insert(m1)

    for j in items:
        tree.insert(j)
    print(c_node.count_cur_stat())
    c_node.archive()
    for j in items:
        assert j in tree
    print(c_node.count_cur_stat())
    c_node.archive()
    for j in items:
        tree.remove(j)
    print(c_node.count_cur_stat())
    c_node.archive()
    for j in items:
        assert j not in tree
    print(c_node.count_cur_stat())
    c_node.archive()

    assert m1 in tree
    tree.remove(m1)
    assert m1 not in tree
    print(c_node.count_cur_stat())
    c_node.archive()

    stat = c_node.count_stat()

    print(stat)
    lt = sum(map(lambda x: x[0], stat))
    eq = sum(map(lambda x: x[1], stat))

    print("Skupno je bilo opravljeno:", lt, "prevejranj po velikosti (<),", eq,
          "preverjan enakosti (==)", "in skupno", lt + eq, "preverjanj.")


def main() -> None:
    # RedBlackTree zamenjaj s svojim drevesom, ter preveri, kako deluje
    # start = process_time()
    # test_adding(RedBlackTree(), 10000)
    # print("Simple test: {time} s".format(time=(process_time() - start)))
    # start = process_time()
    # count_adding(RedBlackTree(), 1000)
    # print("Simple test: {time} s".format(time=(process_time() - start)))
    start = process_time()
    count_adding(NaiveTree(), 1000)
    print("Simple test: {time} s".format(time=(process_time() - start)))


if __name__ == '__main__':
    main()
