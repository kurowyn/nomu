from src.machine import Machine
from src.models import Beverage

def main() -> None:
    BEVERAGE_NAMES = [
        'Soda-1',
        'Soda-2',
        'Pepsi',
        'Cocacola',
        'Sprite',
        'Orange Juice',
    ]

    BEVERAGES = [Beverage(name=name, price=100 * i, quantity=5 * i)
                 for i, name in enumerate(BEVERAGE_NAMES, start=1)]

    Machine(BEVERAGES).begin()


if __name__ == '__main__':
    main()