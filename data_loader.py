import os
from models import (
    MenuItem, Main_Dish, Appetizer, Pasta, Noodle, Rice, Soup,
    Dessert, Coffee_Types, Burrito, Alcoholic_Drink, Maultasche,
    Extras, Non_Alcoholic_Drink, Taco, Pizza, Döner, Pide, Burger, Restaurant
)

def load_data_from_csv(master_csv_path="data/restaurants.csv"):

    class_mapping = {
        "Main_Dish": Main_Dish, "Appetizer": Appetizer, "Pasta": Pasta,
        "Noodle": Noodle, "Rice": Rice, "Soup": Soup, "Dessert": Dessert,
        "Coffee_Types": Coffee_Types, "Burrito": Burrito, "Alcoholic_Drink": Alcoholic_Drink,
        "Maultasche": Maultasche, "Extras": Extras, "Non_Alcoholic_Drink": Non_Alcoholic_Drink,
        "Taco": Taco, "Pizza": Pizza , "Döner" : Döner, "Pide" : Pide, "Burger": Burger
    }

    restaurants_pool = []

    if not os.path.exists(master_csv_path):
        print(f"Fehler: Master-Datei '{master_csv_path}' wurde nicht gefunden.")
        return restaurants_pool

    with open(master_csv_path, mode="r", encoding="utf-8-sig") as master_file:
        lines = master_file.readlines()
        if not lines:
            return restaurants_pool

        for line in lines[1:]:
            line_str = line.strip()
            if not line_str: continue

            parts = line_str.split(",")
            if len(parts) < 3: continue

            name = parts[0].strip()
            cuisine = parts[1].strip()
            menu_filename = parts[2].strip()

            # WICHTIG: Pfad zum 'data'-Ordner hinzufügen
            full_menu_path = os.path.join("data", menu_filename)
            menu_items = []

            if os.path.exists(full_menu_path):
                with open(full_menu_path, mode="r", encoding="utf-8-sig") as menu_file:
                    menu_lines = menu_file.readlines()
                    if len(menu_lines) > 1:
                        for item_line in menu_lines[1:]:
                            item_str = item_line.strip()
                            if not item_str: continue

                            item_parts = item_str.rsplit(",", 2)
                            if len(item_parts) == 3:
                                item_name = item_parts[0].strip().strip('"')
                                category_str = item_parts[1].strip()
                                price_str = item_parts[2].strip()

                                try:
                                    price = float(price_str)
                                    class_blueprint = class_mapping.get(category_str, MenuItem)
                                    menu_items.append(class_blueprint(item_name, price))
                                except ValueError:
                                    print(f"⚠️ Warnung: Zeile konnte nicht geparst werden: {item_str}")
            else:
                print(f"ℹ️ Hinweis: Menüdatei '{full_menu_path}' fehlt für '{name}'.")

            restaurants_pool.append(Restaurant(name, cuisine, menu_items))

    return restaurants_pool