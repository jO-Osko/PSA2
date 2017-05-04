import importlib
from typing import TypeVar, List

from tree.AbstractTree import AbstractTree

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
    #("FilipKoprivec", "RedBlackTree", "RedBlackTree", "b"),
    #("EvaErzin", "SplayTree", "SplayTree", "g"),
    # ("SamoKralj_234Tree", "Tree234", "Tree_234", "c"),
    #("ZigaZupancic", "BTree", "BTree", "m"),
    #("KevinStampar", "Treap", "Treap", "y"),
    #("LukaAvbreht", "AvlTree", "AvlTree", "k"),
    #("NinaSlivnik", "MyList", "SkipList", "#add8e6")
    ("vzorec", "BplusTree", "BplusTree", "k"),
]


def import_helper(user_name: str, file_name: str, class_name: str, prefix: str = "tree") -> Type[T]:
    tree = getattr(importlib.import_module(".".join([prefix, user_name, file_name])), class_name)
    return tree


def get_users(add_naive: bool = False):
    users = []  # type: List[UserData]
    trees_data = trees
    if not add_naive:
        trees_data = filter(lambda x: x[0] != "vzorec", trees_data)
    for user_name, file_name, class_name, color_code in trees_data:
        users.append(UserData(user_name, file_name, class_name,
                              import_helper(user_name, file_name, class_name),
                              color_code))
    return users


def main() -> None:
    pass


if __name__ == '__main__':
    main()
