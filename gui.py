import tkinter as tk
from tkinter import messagebox
from models import Order
from PIL import Image, ImageTk # Import Pillow for image handling

class AalenEatsApp:
    """Hauptanwendungsklasse für das GUI-Layout mit Scrollbars."""

    def __init__(self, root, restaurant_data):
        self.root = root
        self.root.title("AalenEats - Restaurant Selector")
        self.root.geometry("400x600")

        self.restaurants = restaurant_data
        self.current_order = Order()

        self.logo_image = None # To keep a reference to the image, preventing garbage collection

        self.show_start_screen() # Start with the new welcome screen

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

    def show_start_screen(self):
        """Zeigt den Startbildschirm mit Logo und "Start Ordering"-Button."""
        container = self.create_scrollable_container()

        tk.Label(container, text="Welcome to Aalen Eats", font=("Helvetica", 24, "italic")).pack(pady=20)

        try:
            # Load the image
            original_image = Image.open("data/logo_last.png") # Corrected image path
            # Resize image to fit (optional, adjust size as needed)
            resized_image = original_image.resize((200, 200), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(resized_image)
            tk.Label(container, image=self.logo_image).pack(pady=10)
        except FileNotFoundError:
            tk.Label(container, text="Logo not found: data/logo_last.png", fg="red").pack(pady=10)
        except Exception as e:
            tk.Label(container, text=f"Error loading logo: {e}", fg="red").pack(pady=10)


        tk.Button(container, text="Start Ordering", font=("Arial", 14, "bold"), bg="green", fg="white",
                  command=self.show_cuisine_selection).pack(pady=30)

    def show_cuisine_selection(self):
        """Schritt 1: Küchen anzeigen."""
        container = self.create_scrollable_container()

        tk.Label(container, text="Welcome to AalenEats", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(container, text="What would you like to eat?", font=("Helvetica", 12)).pack(pady=5)

        # Display cart summary on the home screen
        if self.current_order.selected_items:
            order_summary_frame = tk.Frame(container)
            order_summary_frame.pack(pady=5) # This frame will be centered

            tk.Label(order_summary_frame, text="Your Current Order:", font=("Arial", 12, "bold")).pack()
            for item in self.current_order.selected_items:
                tk.Label(order_summary_frame, text=f"- {item.name} ({item.price:.2f}€)", font=("Arial", 10)).pack()
            total = self.current_order.get_total_price()
            tk.Label(order_summary_frame, text=f"Total: {total:.2f}€", font=("Arial", 12, "bold"), fg="green").pack(pady=5)
            tk.Button(order_summary_frame, text="View Full Cart", command=lambda: self.show_cart(None, None)).pack(pady=5) # Pass None for restaurant and category as they are not relevant here

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

        # Navigation Buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=20)
        tk.Button(nav_frame, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Home", fg="blue", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="left", padx=5)

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

        # Navigation Buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=20)
        tk.Button(nav_frame, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=lambda: self.show_restaurant_list(restaurant.cuisine_type)).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Home", fg="blue", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="left", padx=5)

    def _update_menu_item_quantity(self, item, quantity_change, restaurant, selected_category):
        # Get current quantity from order
        current_quantity = self.current_order.selected_items.get(item.id, {}).get('quantity', 0)
        new_quantity = current_quantity + quantity_change

        if new_quantity > 0:
            self.current_order.set_item_quantity(item, new_quantity)
        else:
            # If new_quantity is 0 or less, remove the item from the cart
            if item.id in self.current_order.selected_items:
                del self.current_order.selected_items[item.id]

        # Refresh the entire menu to reflect the quantity change
        self.show_menu(restaurant, selected_category)

    def show_menu(self, restaurant, selected_category):
        """Schritt 4: Filtert Gerichte."""
        container = self.create_scrollable_container()

        tk.Label(container, text=f"{restaurant.name}", font=("Helvetica", 16, "bold")).pack(pady=5)
        tk.Label(container, text=selected_category.__name__.replace("_", " "), font=("Helvetica", 14, "italic"), fg="gray").pack(pady=5)

        # Top navigation and info frame for Back/Home and "Click items..." text
        top_nav_and_info_frame = tk.Frame(container)
        top_nav_and_info_frame.pack(pady=5, fill="x") # Keep fill="x" to spread buttons

        tk.Button(top_nav_and_info_frame, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=lambda: self.show_category_selection(restaurant)).pack(side="left", padx=5)

        tk.Label(top_nav_and_info_frame, text="Adjust quantity directly", font=("Arial", 10, "italic")).pack(side="left", expand=True) # Changed text

        tk.Button(top_nav_and_info_frame, text="Home", fg="blue", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="right", padx=5)

        filtered_items = [item for item in restaurant.menu_items if isinstance(item, selected_category)]

        for item in filtered_items:
            item_quantity_frame = tk.Frame(container, bd=1, relief="solid", padx=5, pady=2)
            item_quantity_frame.pack(pady=3, fill="x")

            # Item Name and Price
            tk.Label(item_quantity_frame, text=f"{item.name} ({item.price:.2f}€)",
                     font=("Arial", 10), anchor="w").pack(side="left", expand=True)

            # Quantity controls
            quantity_controls_frame = tk.Frame(item_quantity_frame)
            quantity_controls_frame.pack(side="right")

            current_quantity = self.current_order.selected_items.get(item.id, {}).get('quantity', 0)

            tk.Button(quantity_controls_frame, text="-", font=("Arial", 9, "bold"), width=2,
                      command=lambda i=item: self._update_menu_item_quantity(i, -1, restaurant, selected_category)).pack(side="left")

            # Display current quantity
            quantity_label = tk.Label(quantity_controls_frame, text=str(current_quantity), font=("Arial", 10), width=3)
            quantity_label.pack(side="left", padx=2)

        # New "View Cart" button
        tk.Button(container, text="View Cart", bg="blue", fg="white", font=("Arial", 12, "bold"), width=18,
                  command=lambda: self.show_cart(restaurant, selected_category)).pack(pady=10)

        tk.Button(container, text="Finish & Pay", bg="green", fg="white", font=("Arial", 12, "bold"), width=18,
                  command=self.show_final_receipt).pack(pady=5)

        # Navigation Buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="< Back", fg="red", font=("Arial", 11, "bold"),
                  command=lambda: self.show_category_selection(restaurant)).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Home", fg="blue", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="left", padx=5)

    def add_to_cart(self, item):
        self.current_order.add_item(item)
        messagebox.showinfo("Added", f"{item.name} added to your order!")

    def remove_item_from_cart(self, item_to_remove, restaurant, selected_category):
        # This method is now redundant as update_item_quantity handles removal
        # but keeping it for now if there's a direct 'X' button elsewhere
        self.current_order.remove_item(item_to_remove)
        messagebox.showinfo("Removed", f"{item_to_remove.name} removed from your order!")
        self.show_cart(restaurant, selected_category) # Refresh the cart view

    def clear_current_cart(self, restaurant, selected_category):
        if messagebox.askyesno("Clear Cart", "Are you sure you want to clear your entire cart?"):
            self.current_order.clear_cart()
            messagebox.showinfo("Cart Cleared", "Your cart has been emptied.")
            self.show_cart(restaurant, selected_category) # Refresh the cart view

    def cancel_order(self):
        if messagebox.askyesno("Cancel Order", "Are you sure you want to cancel your entire order and return to the home screen?"):
            self.current_order.clear_cart()
            messagebox.showinfo("Order Canceled", "Your order has been canceled.")
            self.show_cuisine_selection() # Go back to home screen

    def show_cart(self, restaurant, selected_category):
        """Displays the current items in the shopping cart."""
        container = self.create_scrollable_container()

        tk.Label(container, text="Your Shopping Cart", font=("Helvetica", 16, "bold")).pack(pady=10)

        if not self.current_order.selected_items:
            tk.Label(container, text="Your cart is empty.", font=("Arial", 12)).pack(pady=20)
        else:
            cart_frame = tk.Frame(container, bg="#f8f9fa", bd=1, relief="solid")
            cart_frame.pack(pady=10, fill="x", padx=20)

            for item_id, data in self.current_order.selected_items.items():
                item = data['item']
                quantity = data['quantity']

                item_row_frame = tk.Frame(cart_frame, bg="#f8f9fa")
                item_row_frame.pack(fill="x", padx=10, pady=2)

                # Item Name and Price
                tk.Label(item_row_frame, text=f"{item.name[:20]:<20} {item.price:.2f}€",
                         font=("Courier", 11), bg="#f8f9fa", anchor="w").pack(side="left")

                # Quantity adjustment buttons and label
                quantity_frame = tk.Frame(item_row_frame, bg="#f8f9fa")
                quantity_frame.pack(side="right")

                tk.Button(quantity_frame, text="-", font=("Arial", 9, "bold"), width=2,
                          command=lambda i=item: self.update_item_quantity(i, -1, restaurant, selected_category)).pack(side="left")
                tk.Label(quantity_frame, text=f"x{quantity}", font=("Arial", 10), bg="#f8f9fa").pack(side="left", padx=5)
                tk.Button(quantity_frame, text="+", font=("Arial", 9, "bold"), width=2,
                          command=lambda i=item: self.update_item_quantity(i, 1, restaurant, selected_category)).pack(side="left")

            tk.Label(container, text="--------------------------------", font=("Courier", 12)).pack()

            total = self.current_order.get_total_price()
            tk.Label(container, text=f"TOTAL: {total:.2f}€", font=("Courier", 16, "bold"), fg="green").pack(pady=10)

            # Clear Cart Button
            tk.Button(container, text="Clear Cart", bg="orange", fg="white", font=("Arial", 11, "bold"), width=18,
                      command=lambda: self.clear_current_cart(restaurant, selected_category)).pack(pady=10)

        # Navigation Buttons (all in one row, centered)
        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=10)
        if restaurant and selected_category:
            tk.Button(nav_frame, text="< Back to Menu", fg="red", font=("Arial", 11, "bold"),
                      command=lambda: self.show_menu(restaurant, selected_category)).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Home", fg="blue", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Proceed to Checkout", bg="green", fg="white", font=("Arial", 12, "bold"), width=18,
                  command=self.show_final_receipt).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Cancel Order", bg="red", fg="white", font=("Arial", 11, "bold"), width=18,
                  command=self.cancel_order).pack(side="left", padx=5)


    def show_final_receipt(self):
        """Schritt 5: Quittung anzeigen."""
        container = self.create_scrollable_container()

        tk.Label(container, text="Your Receipt", font=("Courier", 18, "bold")).pack(pady=10)

        receipt_frame = tk.Frame(container, bg="#f8f9fa", bd=1, relief="solid")
        receipt_frame.pack(pady=10, fill="x", padx=20)

        for item_id, data in self.current_order.selected_items.items():
            item = data['item']
            quantity = data['quantity']
            tk.Label(receipt_frame, text=f"{item.name[:22]:<22} x{quantity} ... {item.price:.2f}€",
                     font=("Courier", 11), bg="#f8f9fa", anchor="w").pack(fill="x", padx=10, pady=2)

        tk.Label(container, text="--------------------------------", font=("Courier", 12)).pack()

        total = self.current_order.get_total_price()
        tk.Label(container, text=f"TOTAL: {total:.2f}€", font=("Courier", 16, "bold"), fg="green").pack(pady=10)

        tk.Button(container, text="Exit Application", command=self.root.quit, bg="red", fg="white",
                  font=("Arial", 11, "bold"), width=18).pack(pady=15)

        # Navigation Buttons (all in one row, centered)
        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=5)
        tk.Button(nav_frame, text="Cancel Order", bg="red", fg="white", font=("Arial", 11, "bold"), width=18,
                  command=self.cancel_order).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Home", fg="blue", font=("Arial", 11, "bold"),
                  command=self.show_cuisine_selection).pack(side="left", padx=5)