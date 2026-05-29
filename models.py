import uuid

class DomainObject:
    def __init__(self):
        self.id = uuid.uuid4()

class MenuItem(DomainObject):
    def __init__(self, name, price):
        super().__init__()
        self.name = name
        self.price = price

# Spezifische Unterklassen für die Menü-Kategorisierung
class Main_Dish(MenuItem): pass
class Appetizer(MenuItem): pass
class Pasta(MenuItem): pass
class Noodle(MenuItem): pass
class Rice(MenuItem): pass
class Soup(MenuItem): pass
class Dessert(MenuItem): pass
class Coffee_Types(MenuItem): pass
class Burrito(MenuItem): pass
class Alcoholic_Drink(MenuItem): pass
class Maultasche(MenuItem): pass
class Extras(MenuItem): pass
class Non_Alcoholic_Drink(MenuItem): pass
class Taco(MenuItem): pass
class Pizza(MenuItem): pass
class Döner(MenuItem): pass
class Pide(MenuItem): pass
class Burger(MenuItem): pass
class Establishment(DomainObject):
    def __init__(self, name, address="Aalen City Center"):
        super().__init__()
        self.name = name
        self.address = address

class Restaurant(Establishment):
    def __init__(self, name, cuisine_type, menu_items):
        super().__init__(name)
        self.cuisine_type = cuisine_type
        self.menu_items = menu_items  # Liste aus MenuItem-Objekten

class Order:
    """Verwaltet den aktuellen Warenkorb des Kunden."""
    def __init__(self):
        self.selected_items = []

    def add_item(self, item):
        self.selected_items.append(item)

    def get_total_price(self):
        return sum(item.price for item in self.selected_items)