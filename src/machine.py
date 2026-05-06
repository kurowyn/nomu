from .models import Beverage, PurchaseItem, Purchase
from .utils import graceful_input


class Machine:
    def __init__(self, beverages: list[Beverage]) -> None:
        self.purchases = []
        self.beverage_names = [beverage.name for beverage in beverages]
        self.beverage_mapping = {name: beverage for name,
                                 beverage in zip(self.beverage_names, beverages)}
        self.enumerated_beverage_names = {
            i: name for i, name in enumerate(self.beverage_names, start=1)}

    def begin(self):
        while True:
            item = self.select_beverage_menu()
            purchase = self.pay_for_item(item)
            if isinstance(purchase, Purchase):
                self.purchases.append(purchase)

    def search_beverage(self, name: str) -> PurchaseItem | str:
        # Search by number
        if name.isnumeric() and int(name) in self.enumerated_beverage_names:
            beverage = self.beverage_mapping[self.enumerated_beverage_names[int(
                name)]]
        # Search by closest match
        else:
            matches = [beverage for beverage in self.beverage_names if beverage.lower(
            ).startswith(name.lower())]

            if not matches:
                return 'No such beverage.'

            if len(matches) >= 2:
                return 'Ambiguous name. Please be more specific.'

            beverage = self.beverage_mapping[matches[0]]

        if beverage.quantity > 0:
            return PurchaseItem(name=beverage.name, price=beverage.price)
        return 'Beverage out of stock.'


    def display_menu(self) -> None:
        """Displays all beverages in a formatted table with column headers."""
        # Define column widths
        idx_w, name_w, price_w, qty_w = 4, 20, 10, 10

        print("\n" + "=" * (idx_w + name_w + price_w + qty_w))
        # Header row
        print(f"{'#':<{idx_w}} {'NAME':<{name_w}} {'PRICE':<{price_w}} {'QTY':<{qty_w}}")
        print("-" * (idx_w + name_w + price_w + qty_w))

        # Data rows
        for number, name in self.enumerated_beverage_names.items():
            bev = self.beverage_mapping[name]
            print(f"{number:<{idx_w}} {name:<{name_w}} {bev.price:<{price_w}} {bev.quantity:<{qty_w}}")
        print("=" * (idx_w + name_w + price_w + qty_w) + "\n")

    def select_beverage_menu(self) -> PurchaseItem:
        while True:
            self.display_menu()

            user_input = graceful_input('Select a beverage (by shortform name, full name or number): ', exit_message='Selection aborted.').strip()

            result = self.search_beverage(user_input)

            if isinstance(result, PurchaseItem):
                return result
            else:
                print(result)

    def pay_for_item(self, item: PurchaseItem) -> Purchase | int:
        name_w, price_w = 20, 10

        print('PURCHASE')
        print("=" * (name_w + price_w))
        print(f"{'NAME':<{name_w}} {'PRICE':<{price_w}}")
        print(f"{item.name:<{name_w}} {item.price:<{price_w}}")
        print("-" * (name_w + price_w))

        accumulated_pay = 0

        while True:
            pay = graceful_input(
                'Insert money (type c to cancel): ', exit_message='Purchase aborted')

            if pay == 'c':
                print(f'No purchase. Returning money ({accumulated_pay}).')
                return accumulated_pay

            if not pay.isnumeric():
                print('Invalid input.')
                continue

            accumulated_pay += int(pay)

            change = accumulated_pay - item.price

            if change >= 0:
                choice = graceful_input(
                    f"Purchase ready to be finalized, with change {change}. Type c to cancel, or press enter to proceed: ", exit_message='Purchase aborted.')
                if choice == 'c':
                    print(f'No purchase. Returning money ({accumulated_pay}).')
                    return accumulated_pay

                print(
                    f'Purchased {item.name} at the price of {item.price} with change of {change}')

                updated_quantity = self.beverage_mapping[item.name].quantity - 1

                self.beverage_mapping[item.name] = Beverage(
                    name=item.name, price=item.price, quantity=updated_quantity)

                return Purchase(item=item, change=change)

            if change < 0:
                print(
                    f'Not enough money inserted yet. (remaining: {abs(change)})')
