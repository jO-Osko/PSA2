from collections import defaultdict
from typing import Dict, List
from typing import Generic, TypeVar
from typing import Tuple

T = TypeVar("T")


class CountingNode(Generic[T]):
    def __init__(self):
        class InnerCountingNode(Generic[T]):
            c_lt_compare = defaultdict(int)  # type: Dict[Tuple[T,T], int]
            c_same_compare = defaultdict(int)  # type: Dict[Tuple[T,T], int]

            archive = []
            items = []

            def __init__(self, value: T):
                self.value = value
                self.lt_compare = defaultdict(int)
                self.same_compare = defaultdict(int)
                self._archive = []
                InnerCountingNode.items.append(self)

            def __eq__(self, other: "InnerCountingNode") -> bool:
                InnerCountingNode.c_same_compare[(self.value, other.value)] += 1
                self.same_compare[(self.value, other.value)] += 1
                return self.value == other.value

            def __lt__(self, other: "InnerCountingNode") -> bool:
                InnerCountingNode.c_lt_compare[(self.value, other.value)] += 1
                self.lt_compare[(self.value, other.value)] += 1
                return self.value < other.value

            @staticmethod
            def static_reset_count(reset_nodes=True):
                InnerCountingNode.archive.append((InnerCountingNode.c_lt_compare, InnerCountingNode.c_same_compare))
                InnerCountingNode.c_lt_compare = defaultdict(int)
                InnerCountingNode.c_same_compare = defaultdict(int)
                if reset_nodes:
                    for node in InnerCountingNode.items:
                        node.reset_count()  # reset individual nodes

            def reset_count(self):
                self._archive.append((self.lt_compare, self.same_compare))
                self.lt_compare = defaultdict(int)
                self.same_compare = defaultdict(int)

            def __repr__(self):
                return str(self.value)

        self.node_factory = InnerCountingNode

    def create_new_node(self, value: T) -> "InnerCountingNode":
        return self.node_factory(value)

    def get_stat(self):
        return self.node_factory.c_lt_compare, self.node_factory.c_same_compare

    @staticmethod
    def count_stat_from_dict(lt_d, eq_d):
        lt = sum(map(len, lt_d.items()))
        eq = sum(map(len, eq_d.items()))

        return lt, eq, lt + eq

    def count_cur_stat(self) -> Tuple[int, int, int]:
        return CountingNode.count_stat_from_dict(self.node_factory.c_lt_compare, self.node_factory.c_same_compare)

    def count_stat(self) -> List[Tuple[int, int, int]]:
        return [CountingNode.count_stat_from_dict(eq_d, lt_d) for eq_d, lt_d in self.node_factory.archive]

    def archive(self):
        self.node_factory.static_reset_count()