"""Tests intialization for each of the models."""

import pytest
from src.models import Beverage, PurchaseItem, Purchase


def test_beverage_model():
    bev = Beverage(name="Cola", price=150, quantity=10)
    assert bev.name == "Cola"
    assert bev.price == 150
    assert bev.quantity == 10


def test_purchase_item_model():
    item = PurchaseItem(name="Cola", price=150)
    assert item.name == "Cola"
    assert item.price == 150


def test_purchase_model():
    item = PurchaseItem(name="Cola", price=150)
    purchase = Purchase(item=item, change=50)
    assert purchase.item.name == "Cola"
    assert purchase.change == 50
