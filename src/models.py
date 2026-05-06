from typing import NamedTuple

class Beverage(NamedTuple):
    """Simple beverage object."""
    name: str
    price: int
    quantity: int


class PurchaseItem(NamedTuple):
    """Simple purchase object, which represents what a Beverage becomes once purchased."""
    name: str
    price: int


class Purchase(NamedTuple):
    """Just like PurchaseItem, but has change information."""
    item: PurchaseItem
    change: int