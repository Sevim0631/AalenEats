import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from models import Order


class AalenEatsApp:
    """All screens of the AalenEats program."""

    def __init__(self, root, restaurants):
        self.root = root
        self.restaurants = restaurants
        self.order = Order()

        self.root.title("AalenEats - Restaurant Selector")
        self.root.geometry("600x600")
        self.show_start_screen()

    # This method prepares an empty, scrollable page.
    def create_page(self, title, subtitle=""):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, command=canvas.yview)
        page = tk.Frame(canvas)

        page.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=page, anchor="nw", width=580)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"),
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(page, text=title, font=("Arial", 16, "bold")).pack(pady=10)
        if subtitle:
            tk.Label(page, text=subtitle, font=("Arial", 12)).pack(pady=5)

        return page

    # These two buttons are used on most pages.
    def add_navigation(self, page, back_command=None, back_text="< Back"):
        buttons = tk.Frame(page)
        buttons.pack(pady=15)

        if back_command:
            tk.Button(
                buttons,
                text=back_text,
                fg="red",
                command=back_command,
            ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Home",
            fg="blue",
            command=self.show_cuisine_selection,
        ).pack(side="left", padx=5)

    def get_quantity(self, item):
        item_data = self.order.selected_items.get(item.id)
        if item_data:
            return item_data["quantity"]
        return 0

    # ---------- Start and selection pages ----------

    def show_start_screen(self):
        page = self.create_page("Welcome to Aalen Eats")

        try:
            image = Image.open("data/logo_last.png")
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(image)
            tk.Label(page, image=self.logo_image).pack(pady=10)
        except OSError:
            tk.Label(page, text="Logo could not be loaded.", fg="red").pack()

        tk.Button(
            page,
            text="Start Ordering",
            bg="green",
            fg="white",
            font=("Arial", 14, "bold"),
            command=self.show_cuisine_selection,
        ).pack(pady=20)

    def show_cuisine_selection(self):
        page = self.create_page(
            "Welcome to AalenEats",
            "What would you like to eat?",
        )

        # Show the current order when the user returns home.
        if self.order.selected_items:
            summary = tk.Frame(page)
            summary.pack(pady=5)
            tk.Label(summary, text="Your Current Order:", font=("Arial", 12, "bold")).pack()

            for data in self.order.selected_items.values():
                item = data["item"]
                quantity = data["quantity"]
                tk.Label(summary, text=f"{item.name} x{quantity}").pack()

            tk.Label(
                summary,
                text=f"Total: {self.order.get_total_price():.2f} €",
                fg="green",
                font=("Arial", 12, "bold"),
            ).pack(pady=5)
            tk.Button(summary, text="View Full Cart", command=self.show_cart).pack()

        cuisines = sorted({restaurant.cuisine_type for restaurant in self.restaurants})
        for cuisine in cuisines:
            tk.Button(
                page,
                text=cuisine,
                width=20,
                command=lambda cuisine=cuisine: self.show_restaurant_list(cuisine),
            ).pack(pady=5)

    def show_restaurant_list(self, cuisine):
        page = self.create_page(f"{cuisine} Restaurants")

        for restaurant in self.restaurants:
            if restaurant.cuisine_type == cuisine:
                tk.Button(
                    page,
                    text=restaurant.name,
                    width=25,
                    command=lambda restaurant=restaurant: self.show_category_selection(
                        restaurant
                    ),
                ).pack(pady=5)

        self.add_navigation(page, self.show_cuisine_selection)

    def show_category_selection(self, restaurant):
        page = self.create_page(restaurant.name, "Choose a category:")

        categories = {type(item) for item in restaurant.menu_items}
        categories = sorted(categories, key=lambda category: category.__name__)

        for category in categories:
            name = category.__name__.replace("_", " ")
            tk.Button(
                page,
                text=name,
                width=20,
                command=lambda category=category: self.show_menu(restaurant, category),
            ).pack(pady=5)

        go_back = lambda: self.show_restaurant_list(restaurant.cuisine_type)
        self.add_navigation(page, go_back)

    # ---------- Menu page ----------

    def change_menu_quantity(self, item, change, restaurant, category):
        new_quantity = self.get_quantity(item) + change
        self.order.set_item_quantity(item, new_quantity)
        self.show_menu(restaurant, category)

    def show_menu(self, restaurant, category):
        category_name = category.__name__.replace("_", " ")
        page = self.create_page(restaurant.name, category_name)

        for item in restaurant.menu_items:
            if isinstance(item, category):
                row = tk.Frame(page, bd=1, relief="solid", padx=5, pady=3)
                row.pack(fill="x", padx=15, pady=3)

                tk.Label(row, text=f"{item.name} ({item.price:.2f} €)").pack(
                    side="left", expand=True, anchor="w"
                )

                tk.Button(
                    row,
                    text="-",
                    command=lambda item=item: self.change_menu_quantity(
                        item, -1, restaurant, category
                    ),
                ).pack(side="left")
                tk.Label(row, text=str(self.get_quantity(item)), width=3).pack(side="left")
                tk.Button(
                    row,
                    text="+",
                    command=lambda item=item: self.change_menu_quantity(
                        item, 1, restaurant, category
                    ),
                ).pack(side="left")

        actions = tk.Frame(page)
        actions.pack(pady=10)
        tk.Button(
            actions,
            text="View Cart",
            bg="blue",
            fg="white",
            command=lambda: self.show_cart(restaurant, category),
        ).pack(side="left", padx=5)
        tk.Button(
            actions,
            text="Finish & Pay",
            bg="green",
            fg="white",
            command=self.show_final_receipt,
        ).pack(side="left", padx=5)

        go_back = lambda: self.show_category_selection(restaurant)
        self.add_navigation(page, go_back)

    # ---------- Cart page ----------

    def change_cart_quantity(self, item, change, restaurant, category):
        new_quantity = self.get_quantity(item) + change
        self.order.set_item_quantity(item, new_quantity)
        self.show_cart(restaurant, category)

    def clear_cart(self, restaurant=None, category=None):
        answer = messagebox.askyesno("Clear Cart", "Clear the entire cart?")
        if answer:
            self.order.clear_cart()
            self.show_cart(restaurant, category)

    def cancel_order(self):
        answer = messagebox.askyesno("Cancel Order", "Cancel the entire order?")
        if answer:
            self.order.clear_cart()
            self.show_cuisine_selection()

    def show_cart(self, restaurant=None, category=None):
        page = self.create_page("Your Shopping Cart")

        if not self.order.selected_items:
            tk.Label(page, text="Your cart is empty.").pack(pady=20)

        for data in self.order.selected_items.values():
            item = data["item"]
            quantity = data["quantity"]
            row = tk.Frame(page, bd=1, relief="solid", padx=5, pady=3)
            row.pack(fill="x", padx=20, pady=3)

            tk.Label(row, text=f"{item.name} ({item.price:.2f} €)").pack(
                side="left", expand=True, anchor="w"
            )
            tk.Button(
                row,
                text="-",
                command=lambda item=item: self.change_cart_quantity(
                    item, -1, restaurant, category
                ),
            ).pack(side="left")
            tk.Label(row, text=f"x{quantity}", width=4).pack(side="left")
            tk.Button(
                row,
                text="+",
                command=lambda item=item: self.change_cart_quantity(
                    item, 1, restaurant, category
                ),
            ).pack(side="left")

        tk.Label(
            page,
            text=f"TOTAL: {self.order.get_total_price():.2f} €",
            fg="green",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        if self.order.selected_items:
            tk.Button(
                page,
                text="Clear Cart",
                bg="orange",
                command=lambda: self.clear_cart(restaurant, category),
            ).pack(pady=5)

        actions = tk.Frame(page)
        actions.pack(pady=10)
        tk.Button(
            actions,
            text="Proceed to Checkout",
            bg="green",
            fg="white",
            command=self.show_final_receipt,
        ).pack(side="left", padx=5)
        tk.Button(
            actions,
            text="Cancel Order",
            bg="red",
            fg="white",
            command=self.cancel_order,
        ).pack(side="left", padx=5)

        back_to_menu = None
        if restaurant and category:
            back_to_menu = lambda: self.show_menu(restaurant, category)
        self.add_navigation(page, back_to_menu, "< Back to Menu")

    # ---------- Receipt page ----------

    def show_final_receipt(self):
        page = self.create_page("Your Receipt")

        for data in self.order.selected_items.values():
            item = data["item"]
            quantity = data["quantity"]
            line_total = item.price * quantity
            tk.Label(
                page,
                text=f"{item.name[:22]:<22} x{quantity}  {line_total:.2f} €",
                font=("Courier", 11),
            ).pack(anchor="w", padx=30, pady=2)

        tk.Label(
            page,
            text=f"TOTAL: {self.order.get_total_price():.2f} €",
            fg="green",
            font=("Courier", 16, "bold"),
        ).pack(pady=15)

        tk.Button(
            page,
            text="Exit Application",
            bg="red",
            fg="white",
            command=self.root.quit,
        ).pack(pady=10)

        actions = tk.Frame(page)
        actions.pack(pady=5)
        tk.Button(actions, text="Cancel Order", command=self.cancel_order).pack(
            side="left", padx=5
        )
        tk.Button(actions, text="Home", command=self.show_cuisine_selection).pack(
            side="left", padx=5
        )
