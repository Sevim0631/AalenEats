import tkinter as tk
from data_loader import load_data_from_csv
from gui import AalenEatsApp


def main():
    # 1. Daten dynamisch aus dem 'data'-Unterordner laden
    loaded_restaurants = load_data_from_csv("data/restaurants.csv")

    # 2. Tkinter Instanz initialisieren
    root = tk.Tk()

    # 3. GUI mit den geladenen Daten starten
    app = AalenEatsApp(root, loaded_restaurants)

    # 4. App-Schleife starten
    root.mainloop()


if __name__ == "__main__":
    main()