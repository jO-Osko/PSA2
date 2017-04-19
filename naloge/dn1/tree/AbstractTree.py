# -*- coding: utf-8 -*-
from typing import Generic, Iterable, TypeVar, Optional, Iterator, MutableMapping

T = TypeVar("T")


class AbstractTree(Generic[T]):
    def __init__(self, data: Optional[Iterable[T]] = None) -> None:
        pass

    def insert(self, item: T) -> None:
        """
        Vstavi element item v iskalno drevo, če ta element že obstaja ga prepišemo z novim
        :param item: Element, ki ga vstavljamo v drevo
        :return: None
        """
        raise NotImplementedError("Not implemented")

    def remove(self, item: T) -> None:
        """
        Odstrani element item iz iskalnega drevesa, če ga ni naj metoda sproži ValueError
        :param item: Element, ki ga brišemo iz drevesa
        :return: None
        """
        raise NotImplementedError("Not implemented")

    def search(self, item: T) -> bool:
        """
        Vrne True, če se item nahaja v drevesu in False, če se ne.
        :param item: Element, ki ga v drevesu iščemo
        :return: True če se item nahaja v drevesu, drugače False.
        """
        raise NotImplementedError("Not implemented")

    def __contains__(self, item: T) -> bool:
        return self.search(item)

"""
Če implementirate metode v tem drevesu, potem lahko drevo s pomočjo TreeDict brez težav pretvorimo v slovar, 
to pa vsekakor ni pogoj za domačo nalogo.
"""
class AbstractSearchTree(AbstractTree, Generic[T]):

    def find(self, item: T) -> T:
        """
        Vrne vrednost v drevesu, ki je enaka item, če se item nahaja v drevesu, drugače pa sproži ValueError
        :param item: Element, ki ga iščemo
        :return: Element v drevesu
        """
        raise NotImplementedError("Not implemented")

    def search(self, item: T) -> bool:
        try:
            self.find(item)
            return True
        except ValueError:
            return False

    def in_order_traversal(self) -> Iterator[T]:
        raise NotImplementedError("Not implemented")

    def size(self) -> int:
        raise NotImplementedError("Not implemented")

    def __len__(self) -> int:
        return self.size()