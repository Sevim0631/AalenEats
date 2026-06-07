import uuid

class DomainObject:
    def __init__(self):
        self.id = uuid.uuid4()

class MenuItem(DomainObject):
    def __init__(self, name, price):
        super().__init__()
        self.name = name
        self.price = price

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

# Restaurant now inherits directly from DomainObject
class Restaurant(DomainObject):
    def __init__(self, name, cuisine_type, menu_items):
        super().__init__()
        self.name = name
        self.cuisine_type = cuisine_type
        self.menu_items = menu_items  # Liste aus MenuItem-Objekten

class Order:
    def __init__(self):
        self.selected_items = []

    def add_item(self, item):
        self.selected_items.append(item)

    def remove_item(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)

    def clear_cart(self):
        self.selected_items.clear()

    def get_total_price(self):
        return sum(item.price for item in self.selected_items)