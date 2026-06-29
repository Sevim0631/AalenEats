import os
from models import (
    MenuItem, Main_Dish, Appetizer, Pasta, Noodle, Rice, Soup,
    Dessert, Coffee_Types, Burrito, Alcoholic_Drink, Maultasche,
    Extras, Non_Alcoholic_Drink, Taco, Pizza, Döner, Pide, Burger, Restaurant
)

def load_data_from_csv(master_csv_path="data/restaurants.csv"):

    class_mapping = {
        "Pizza": Pizza,
        "Burger": Burger,
        "Pasta": Pasta,
        "Dessert": Dessert,
        "Main_Dish": Main_Dish,
        "Appetizer": Appetizer,
        "Soup": Soup,
        "Rice": Rice,
        "Noodle": Noodle,
        "Coffee_Types": Coffee_Types,
        "Burrito": Burrito,
        "Alcoholic_Drink": Alcoholic_Drink,
        "Maultasche": Maultasche,
        "Extras": Extras,
        "Non_Alcoholic_Drink": Non_Alcoholic_Drink,
        "Taco": Taco,
        "Döner": Döner,
        "Pide": Pide,
    }

    restaurants_pool = []

    restaurants = pd.read_csv("data/restaurants.csv")

    for name, cuisine, menu_file in zip(
        restaurants["Restaurant Name"],
        restaurants["Cuisine"],
        restaurants["Menu File"]
    ):
        print("Loading:", menu_file)
        menu = pd.read_csv("data/" + menu_file)
        menu_items = []

        menu = pd.read_csv("data/" + menu_file)

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
                                    print(f"fıle could not be parsed: {item_str}")
            else:
                print(f" Menufile '{full_menu_path}' missing for '{name}'.")

            restaurants_pool.append(Restaurant(name, cuisine, menu_items))

    return restaurants_pool