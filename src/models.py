from typing import NamedTuple

class Beverage(NamedTuple):
    name: str
    price: int
    quantity: int


class PurchaseItem(NamedTuple):
    name: str
    price: int


class Purchase(NamedTuple):
    item: PurchaseItem
    change: int