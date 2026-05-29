import tkinter as tk
from data_loader import load_data_from_csv
from gui import AalenEatsApp


def main():
    loaded_restaurants = load_data_from_csv("data/restaurants.csv")

    root = tk.Tk()

    app = AalenEatsApp(root, loaded_restaurants)

    root.mainloop()


if __name__ == "__main__":
    main()