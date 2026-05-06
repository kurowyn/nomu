"""Tests machine logic. Has the most amount of tests."""

from src.machine import Machine
from src.models import Beverage, Purchase, PurchaseItem
import pytest


@pytest.fixture
def machine():
    """Provides a fresh Machine instance for each test."""
    beverages = [
        Beverage("Apple Juice", 100, 5),
        Beverage("Orange Juice", 500, 10),  
        Beverage("Grape Soda", 300, 6)    
    ]
    return Machine(beverages)

# --- Search Logic Tests ---


def test_search_by_number(machine):
    result = machine.search_beverage("1")
    assert isinstance(result, PurchaseItem)
    assert result.name == "Apple Juice"
    assert result.price == 100


def test_search_by_exact_string(machine):
    result = machine.search_beverage("Grape Soda")
    assert result.name == "Grape Soda"


def test_search_by_prefix_string(machine):
    result = machine.search_beverage("Orang")
    assert result.name == "Orange Juice"


def test_search_ambiguous(machine):
    # Add a conflicting beverage to trigger ambiguity
    machine.beverage_names.append("Apple Soda")
    machine.beverage_mapping["Apple Soda"] = Beverage("Apple Soda", 100, 5)

    result = machine.search_beverage("App")
    assert result == 'Ambiguous name. Please be more specific.'


def test_search_no_match(machine):
    result = machine.search_beverage("Water")
    assert result == 'No such beverage.'


def test_search_out_of_stock(machine):
    # Deplete stock
    machine.beverage_mapping["Apple Juice"] = Beverage("Apple Juice", 100, 0)
    result = machine.search_beverage("Apple Juice")
    assert result == 'Beverage out of stock.'

# --- Payment Logic Tests ---


def test_pay_for_item_success_exact_change(machine, monkeypatch):
    item = PurchaseItem("Apple Juice", 100)

    # User inputs: 100, then Enter to proceed
    inputs = iter(["100", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    purchase = machine.pay_for_item(item)
    assert isinstance(purchase, Purchase)
    assert purchase.item.name == "Apple Juice"
    assert purchase.change == 0
    # Stock decreased
    assert machine.beverage_mapping["Apple Juice"].quantity == 4


def test_pay_for_item_success_with_change(machine, monkeypatch):
    item = PurchaseItem("Apple Juice", 100)

    # User inputs: 50, 60 (total 110), then Enter to proceed
    inputs = iter(["50", "60", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    purchase = machine.pay_for_item(item)
    assert purchase.change == 10


def test_pay_for_item_cancel_during_insert(machine, monkeypatch):
    item = PurchaseItem("Apple Juice", 100)

    # User inputs: 50, then 'c' to cancel
    inputs = iter(["50", "c"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = machine.pay_for_item(item)
    assert result == 50  # Returns accumulated pay
    # Stock unmodified
    assert machine.beverage_mapping["Apple Juice"].quantity == 5


def test_pay_for_item_cancel_at_checkout(machine, monkeypatch):
    item = PurchaseItem("Apple Juice", 100)

    # User inputs: 100, then 'c' to cancel at the final prompt
    inputs = iter(["100", "c"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = machine.pay_for_item(item)
    assert result == 100  # Returns accumulated pay


def test_pay_for_item_invalid_input_ignored(machine, monkeypatch):
    item = PurchaseItem("Apple Juice", 100)

    # User inputs: 'abc' (invalid), '100' (valid), Enter (proceed)
    inputs = iter(["abc", "100", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    purchase = machine.pay_for_item(item)
    assert isinstance(purchase, Purchase)
    assert purchase.change == 0

# --- Menu Selection Tests ---


def test_select_beverage_menu_valid(machine, monkeypatch):
    # Simulate typing '1' at the menu prompt
    monkeypatch.setattr('builtins.input', lambda _: "1")

    item = machine.select_beverage_menu()
    assert isinstance(item, PurchaseItem)
    assert item.name == "Apple Juice"


def test_select_beverage_menu_retry_on_invalid(machine, monkeypatch):
    # Simulate invalid input ("Water"), then valid input ("1")
    inputs = iter(["Water", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    item = machine.select_beverage_menu()
    assert item.name == "Apple Juice"

# --- Main App Loop Test ---


def test_begin_loop_termination(machine, monkeypatch):
    # The begin() method loops infinitely. We can test it by forcing a SystemExit
    # during the menu selection phase to ensure it calls select_beverage_menu.
    def mock_input(_):
        raise EOFError

    monkeypatch.setattr('builtins.input', mock_input)

    with pytest.raises(SystemExit):
        machine.begin()
