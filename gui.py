import tkinter as tk
from tkinter import messagebox
from models import Order

class AalenEatsApp:
    """Hauptanwendungsklasse für das GUI-Layout mit Scrollbars."""

    def __init__(self, root, restaurant_data):
        self.root = root
        self.root.title("AalenEats - Restaurant Selector")
        self.root.geometry("400x600")

        self.restaurants = restaurant_data
        self.current_order = Order()

        self.show_cuisine_selection()

    def create_scrollable_container(self):
        """Erzeugt ein scrollbares Canvas mit Mausrad-Unterstützung."""
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=400)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        return scrollable_frame

    def show_cuisine_selection(self):
        """Schritt 1: Küchen anzeigen."""
        container = self.create_scrollable_container()

        tk.Label(container, text="Welcome to AalenEats", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(container, text="What would you like to eat?", font=("Helvetica", 12)).pack(pady=5)

        cuisines = sorted(list(set(r.cuisine_type for r in self.restaurants)))

        for cuisine in cuisines:
            btn = tk.Button(container, text=cuisine, font=("Arial", 12), width=20,
                            command=lambda c=cuisine: self.show_restaurant_list(c))
            btn.pack(pady=5)

    def show_restaurant_list(self, selected_cuisine):
        """Schritt 2: Restaurants anzeigen."""
        container = self.create_scrollable_container()

        tk.Label(container, text=f"{selected_cuisine} Restaurants", font=("Helvetica", 16, "bold")).pack(pady=10)

        matching_restaurants = [r for r in self.restaurants if r.cuisine_type == selected_cuisine]

        for rest in matching_restaurants:
            btn = tk.Button(container, text=rest.name, font=("Arial", 12), width=20,
                            command=lambda r=rest: self.show_category_selection(r))
            btn.pack(pady=5)

        tk.Button(container, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(pady=20)

    def show_category_selection(self, restaurant):
        """Schritt 3: Kategorienabfrage anzeigen."""
        container = self.create_scrollable_container()

        tk.Label(container, text=restaurant.name, font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(container, text="Choose a category:", font=("Helvetica", 12)).pack(pady=5)

        categories = set(type(item) for item in restaurant.menu_items)
        sorted_categories = sorted(list(categories), key=lambda cls: cls.__name__)

        for cls in sorted_categories:
            category_display_name = cls.__name__.replace("_", " ")

            btn = tk.Button(container, text=category_display_name, font=("Arial", 12), width=20,
                            command=lambda r=restaurant, c=cls: self.show_menu(r, c))
            btn.pack(pady=5)

        tk.Button(container, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=lambda: self.show_restaurant_list(restaurant.cuisine_type)).pack(pady=20)

    def show_menu(self, restaurant, selected_category):
        """Schritt 4: Filtert Gerichte."""
        container = self.create_scrollable_container()

        category_name = selected_category.__name__.replace("_", " ")
        tk.Label(container, text=f"{restaurant.name}", font=("Helvetica", 16, "bold")).pack(pady=5)
        tk.Label(container, text=category_name, font=("Helvetica", 14, "italic"), fg="gray").pack(pady=5)
        tk.Label(container, text="Click items to add to order", font=("Arial", 10, "italic")).pack(pady=5)

        filtered_items = [item for item in restaurant.menu_items if isinstance(item, selected_category)]

        for item in filtered_items:
            display_text = f"{item.name}\n{item.price:.2f}€"

            btn = tk.Button(container, text=display_text, font=("Arial", 10), width=42, height=2,
                            wraplength=320, justify="center",
                            command=lambda i=item: self.add_to_cart(i))
            btn.pack(pady=3)

        tk.Button(container, text="Finish & Pay", bg="green", fg="white", font=("Arial", 12, "bold"), width=18,
                  command=self.show_final_receipt).pack(pady=15)

        tk.Button(container, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=lambda: self.show_category_selection(restaurant)).pack(pady=10)

    def add_to_cart(self, item):
        self.current_order.add_item(item)
        messagebox.showinfo("Added", f"{item.name} added to your order!")

    def show_final_receipt(self):
        """Schritt 5: Quittung anzeigen."""
        container = self.create_scrollable_container()

        tk.Label(container, text="Your Receipt", font=("Courier", 18, "bold")).pack(pady=10)

        receipt_frame = tk.Frame(container, bg="#f8f9fa", bd=1, relief="solid")
        receipt_frame.pack(pady=10, fill="x", padx=20)

        for item in self.current_order.selected_items:
            tk.Label(receipt_frame, text=f"{item.name[:22]:<22} ... {item.price:.2f}€",
                     font=("Courier", 11), bg="#f8f9fa", anchor="w").pack(fill="x", padx=10, pady=2)

        tk.Label(container, text="--------------------------------", font=("Courier", 12)).pack()

        total = self.current_order.get_total_price()
        tk.Label(container, text=f"TOTAL: {total:.2f}€", font=("Courier", 16, "bold"), fg="green").pack(pady=10)

        tk.Button(container, text="Exit Application", command=self.root.quit, bg="red", fg="white",
                  font=("Arial", 11, "bold"), width=18).pack(pady=15)