import tkinter as tk
import datetime
import json


class OrderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("2Rendelés")
        self.master.attributes("-fullscreen", True)
        with open("menu.json") as f:
            self.menu_items = json.load(f)
            for item in self.menu_items:
                item['quantity'] = 0

        self.order = []
        self.total_price = 0

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=3)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(3, weight=1)

        menu_frame = tk.Frame(self.master, bg="white smoke", width=400)
        menu_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)

        menu_label = tk.Label(menu_frame, text="Menü", font=("Courier New", 21))
        menu_label.pack(pady=10)
        self.menu_listbox = tk.Listbox(menu_frame, font=("Courier New", 17), width=70, bg="snow")
        category_colors = {
            "Menus": "#ADD8E6",
            "Sides": "#90EE90",
            "Pizza": "#FFFFE0",
            "Desserts": "#FFB6C1",
            "Drinks": "#E6E6FA",
        }
        self.menu_listbox = tk.Listbox(menu_frame, font=("Courier New", 17), width=70, bg="snow")
        for item in self.menu_items:
            category = item['category']
            color = category_colors.get(category, "white")
            self.menu_listbox.insert(tk.END, f"{item['name']:.<59}{item['price']: >5} Lei")
            self.menu_listbox.itemconfig(tk.END, bg=color)
            self.menu_listbox.pack(pady=10)
        self.menu_listbox.config(height=50)
        self.menu_listbox.bind('<Double-Button-1>', self.add_item)
        order_frame = tk.Frame(self.master, bg="white smoke", width=300)
        order_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)
        order_label = tk.Label(order_frame, text="Rendelés", font=("Courier New", 21), bg="white smoke")
        order_label.pack(pady=10)
        self.order_listbox = tk.Listbox(order_frame, font=("Courier New", 14), width=50, bg="snow")
        self.order_listbox.pack(pady=10)

        remove_button = tk.Button(order_frame, text="Elem eltávolitása", font=("Courier New", 16), width=40,
                                  height=2, command=self.delete_item)
        remove_button.pack(pady=10)
        reduce_button = tk.Button(order_frame, text="Mennyiség csökkentése", font=("Courier New", 16), width=40,
                                  height=2, command=self.decrease_quantity)
        reduce_button.pack(pady=10)
        place_order_button = tk.Button(order_frame, text="Rendelés", font=("Courier New", 16), width=40, height=3,
                                       bg="#B7CE9E", command=self.place_order)
        place_order_button.pack(pady=10)
        exit_button = tk.Button(self.master, text="Kilépés", font=("Courier New", 17), width=20, height=1,
                                bg="light coral", command=self.master.destroy)
        exit_button.grid(row=4, column=1, sticky="w", padx=120, pady=25)

        self.menu_listbox.bind("<Double-Button-1>", self.add_item)

    def add_item(self, event=None):
        if event:
            selection = event.widget.curselection()
        else:
            selection = self.menu_listbox.curselection()

        if selection:
            item = self.menu_items[selection[0]]
            name = item['name']
            price = item['price']
            item_found = False
            for i in range(self.order_listbox.size()):
                if self.order_listbox.get(i).startswith(name):
                    item['quantity'] += 1
                    self.total_price += price
                    self.order_listbox.delete(0, tk.END)
                    for item in self.order:
                        name = item['name']
                        price = item['price']
                        quantity = item['quantity']
                        new_price = quantity * price
                        self.order_listbox.insert(tk.END, f"{name} x {quantity} - {new_price} Lei")
                    item_found = True
                    break
            if not item_found:
                item['quantity'] = 1
                self.order_listbox.insert(tk.END, f"{name} x 1 - {price} Lei")
                self.order.append(item)
                self.total_price += price

    def delete_item(self):
        selection = self.order_listbox.curselection()
        if selection:
            item = self.order[selection[0]]
            self.total_price -= item['price'] * item['quantity']
            self.order_listbox.delete(selection[0])
            self.order.remove(item)
            item['quantity'] = 0

    def decrease_quantity(self):
        selection = self.order_listbox.curselection()
        if selection:
            item = self.order[selection[0]]
            name = item['name']
            price = item['price']
            item['quantity'] -= 1
            quantity = item['quantity']
            if quantity == 0:
                self.order_listbox.delete(selection[0])
                self.order.remove(item)
                self.total_price -= price
            else:
                new_price = quantity * price
                self.order_listbox.delete(selection[0])
                self.order_listbox.insert(selection[0], f"{name} x {quantity} - {new_price} Lei")
                self.total_price -= price

    def place_order(self):
        if not self.order:
            return
        grouped_order = {}
        for item in self.order:
            if item['category'] not in grouped_order:
                grouped_order[item['category']] = []
            grouped_order[item['category']].append(item)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        order_items = ""
        order_receipt = ""
        for category, items in grouped_order.items():
            order_items += f"{category.capitalize()}:\n"
            for item in items:
                order_items += f"{item['name']} " \
                               f"{item['price']} x {item['quantity']} - {item['price'] * item['quantity']} Lei\n"
            order_items += "\n"
            order_receipt = f"{'-' * 30}\n{'Számla':^30}\n{'-' * 30}\n{order_items}\n{'-' * 30}\n{'Total:':>23}" \
                            f"{self.total_price:>7} Lei\n{'-' * 30}\n{'Rendelés dátuma:':<17}" \
                            f"\n{timestamp:>13}\n{'-' * 30}"
        receipt_window = tk.Toplevel(self.master)
        receipt_window.title("Rendelési nyugta")
        receipt_window.geometry("400x500")
        receipt_label = tk.Label(receipt_window, text=order_receipt)
        receipt_label.pack(fill=tk.BOTH, expand=True)
        with open(f"{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write(order_receipt)
        self.order = []
        self.total_price = 0
        for item in self.menu_items:
            item['quantity'] = 0
        self.order_listbox.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white smoke")
    app = OrderApp(root)
    root.mainloop()
