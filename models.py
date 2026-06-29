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
        self.menu_items = menu_items if menu_items is not None else [] # Liste aus MenuItem-Objekten

class Order:
    def __init__(self):
        self.selected_items = {} # Changed to dictionary to store item and quantity

    def add_item(self, item, quantity=1):
        if item.id in self.selected_items:
            self.selected_items[item.id]['quantity'] += quantity
        else:
            self.selected_items[item.id] = {'item': item, 'quantity': quantity}

    def remove_item(self, item, quantity=1):
        if item.id in self.selected_items:
            self.selected_items[item.id]['quantity'] -= quantity
            if self.selected_items[item.id]['quantity'] <= 0:
                del self.selected_items[item.id]

    def set_item_quantity(self, item, quantity):
        if quantity <= 0:
            if item.id in self.selected_items:
                del self.selected_items[item.id]
        else:
            self.selected_items[item.id] = {'item': item, 'quantity': quantity}

    def clear_cart(self):
        self.selected_items.clear()

    def get_total_price(self):
        return sum(data['item'].price * data['quantity'] for data in self.selected_items.values())