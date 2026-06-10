# -*- coding: utf-8 -*-
# =============================================================================
#  McJin Point of Sale System
#  GUI built with tkinter
#  Fully modularized -- one function per responsibility
#
#  Python Built-in Functions used (requirement):
#   1. len()    -- counts the number of items in the current order
#   2. sum()    -- computes the grand total from the sales list
#   3. sorted() -- sorts menu items alphabetically within a category
#   4. round()  -- rounds the change amount to 2 decimal places
#   5. max()    -- finds the highest-value transaction in sales history
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# =============================================================================
#  CONSTANTS
# =============================================================================

MC_RED      = "#DA291C"
MC_YELLOW   = "#FFC72C"
MC_DARK     = "#27251F"
MC_WHITE    = "#FFFFFF"
MC_LIGHT_BG = "#F5F5F5"
MC_GRAY     = "#E0E0E0"
MC_GREEN    = "#264F36"

CREDENTIALS = {
    "admin":    "admin123",
    "cashier1": "pass1",
    "cashier2": "pass2",
}

MENU_ITEMS = {
    # Burgers
    "B01": ("Big Mac",                   "Burgers",   5.99),
    "B02": ("Quarter Pounder w/ Cheese", "Burgers",   6.49),
    "B03": ("McDouble",                  "Burgers",   3.99),
    "B04": ("McChicken",                 "Burgers",   3.49),
    "B05": ("Filet-O-Fish",              "Burgers",   4.49),
    "B06": ("Hamburger",                 "Burgers",   1.99),
    "B07": ("Cheeseburger",              "Burgers",   2.29),
    # Chicken
    "C01": ("10pc Chicken McNuggets",    "Chicken",   5.49),
    "C02": ("6pc Chicken McNuggets",     "Chicken",   3.79),
    "C03": ("Crispy Chicken Sandwich",   "Chicken",   5.29),
    "C04": ("Spicy McChicken",           "Chicken",   3.79),
    # Fries & Sides
    "S01": ("Large Fries",               "Sides",     3.29),
    "S02": ("Medium Fries",              "Sides",     2.79),
    "S03": ("Small Fries",               "Sides",     2.29),
    "S04": ("Apple Slices",              "Sides",     1.49),
    "S05": ("Side Salad",                "Sides",     3.49),
    # Drinks
    "D01": ("Large Coca-Cola",           "Drinks",    2.49),
    "D02": ("Medium Coca-Cola",          "Drinks",    1.99),
    "D03": ("Small Coca-Cola",           "Drinks",    1.49),
    "D04": ("Large Coffee",              "Drinks",    2.29),
    "D05": ("McCafe Latte",              "Drinks",    3.99),
    "D06": ("Chocolate Milkshake",       "Drinks",    3.79),
    "D07": ("Orange Juice",              "Drinks",    2.49),
    # Breakfast
    "K01": ("Egg McMuffin",              "Breakfast", 4.19),
    "K02": ("Sausage McMuffin",          "Breakfast", 3.69),
    "K03": ("Big Breakfast",             "Breakfast", 6.99),
    "K04": ("Hotcakes",                  "Breakfast", 4.49),
    # Desserts
    "E01": ("McFlurry Oreo",             "Desserts",  3.99),
    "E02": ("Sundae",                    "Desserts",  1.99),
    "E03": ("Apple Pie",                 "Desserts",  1.49),
    "E04": ("Cone",                      "Desserts",  1.09),
}

# =============================================================================
#  BUILT-IN FUNCTION WRAPPERS  (requirement: function for every feature)
# =============================================================================

def count_order_items(order_list):
    """
    Built-in: len()
    Returns the number of distinct item lines in the current order.
    len() returns the number of items in an object (list, string, dict, etc.)
    """
    return len(order_list)


def compute_grand_total(sales_log):
    """
    Built-in: sum()
    Adds up all transaction totals from the sales log dictionary list.
    sum() returns the total sum of all elements in an iterable.
    """
    return sum(record["total"] for record in sales_log)


def get_sorted_menu(category):
    """
    Built-in: sorted()
    Returns menu items for a category sorted A-Z by item name.
    sorted() returns a new sorted list from the elements of an iterable.
    """
    items = [(code, data) for code, data in MENU_ITEMS.items()
             if data[1] == category]
    return sorted(items, key=lambda x: x[1][0])


def compute_change(cash, total):
    """
    Built-in: round()
    Computes change and rounds it to 2 decimal places to avoid float issues.
    round() rounds a number to a specified number of decimal places.
    """
    return round(cash - total, 2)


def get_highest_sale(sales_log):
    """
    Built-in: max()
    Finds the highest-value transaction in the sales log.
    max() returns the largest item in an iterable or among arguments.
    Returns None if no sales yet.
    """
    if not sales_log:
        return None
    return max(sales_log, key=lambda r: r["total"])


# =============================================================================
#  APPLICATION CLASS
# =============================================================================

class McJinPOS(tk.Tk):
    """Root application window -- owns shared state and frame management."""

    def __init__(self):
        super().__init__()
        self.title("McJin POS System")
        self.geometry("1100x700")
        self.resizable(True, True)
        self.configure(bg=MC_DARK)

        self.logged_in_user = tk.StringVar()
        self.sales_log      = []
        self.current_order  = []

        self.container = tk.Frame(self, bg=MC_DARK)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._build_frames()
        self.show_frame("LoginFrame")

    # ------------------------------------------------------------------
    #  Frame management
    # ------------------------------------------------------------------

    def _build_frames(self):
        """Instantiate every screen and stack them in the container."""
        for FrameClass in (LoginFrame, MainMenuFrame, OrderFrame,
                           TotalSalesFrame):
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name):
        """Raise the requested frame to the top."""
        frame = self.frames[frame_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    # ------------------------------------------------------------------
    #  Auth
    # ------------------------------------------------------------------

    def login(self, username, password):
        """Validate credentials using dict.get(). Return True on success."""
        return CREDENTIALS.get(username) == password

    def logout(self):
        """Clear session state and return to login screen."""
        self.logged_in_user.set("")
        self.current_order.clear()
        self.show_frame("LoginFrame")

    # ------------------------------------------------------------------
    #  Order helpers
    # ------------------------------------------------------------------

    def add_to_order(self, code):
        """Add a menu item to the current order (merge duplicates)."""
        if code not in MENU_ITEMS:
            return
        name, _, price = MENU_ITEMS[code]
        for item in self.current_order:
            if item["code"] == code:
                item["qty"] += 1
                return
        self.current_order.append({"code": code, "name": name,
                                   "price": price, "qty": 1})

    def remove_from_order(self, code):
        """Remove one unit of an item; delete the row if qty hits 0."""
        for item in self.current_order:
            if item["code"] == code:
                item["qty"] -= 1
                if item["qty"] <= 0:
                    self.current_order.remove(item)
                return

    def clear_order(self):
        """Clear all items from the current order."""
        self.current_order.clear()

    def get_order_total(self):
        """Return price x qty sum for the current order."""
        return sum(i["price"] * i["qty"] for i in self.current_order)

    def finalize_sale(self, cash_tendered):
        """
        Record the completed transaction.
        Uses round() (built-in #4) for change calculation.
        Returns (total, change) tuple.
        """
        total  = self.get_order_total()
        change = compute_change(cash_tendered, total)   # round() used here
        record = {
            "cashier":   self.logged_in_user.get(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items":     [dict(i) for i in self.current_order],
            "total":     total,
            "cash":      cash_tendered,
            "change":    change,
        }
        self.sales_log.append(record)
        self.clear_order()
        return total, change

    def get_grand_total(self):
        """Uses sum() (built-in #2) to total all recorded transactions."""
        return compute_grand_total(self.sales_log)


# =============================================================================
#  HELPERS
# =============================================================================

def make_mc_button(parent, text, command, bg=MC_YELLOW, fg=MC_DARK,
                   width=18, font_size=11, pady=6):
    """Return a McJin-styled flat button."""
    return tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=MC_RED, activeforeground=MC_WHITE,
        font=("Arial Black", font_size, "bold"),
        relief="flat", cursor="hand2",
        width=width, pady=pady
    )


# =============================================================================
#  SCREEN 1 -- Login
# =============================================================================

class LoginFrame(tk.Frame):
    """Login screen: asks for username and password."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=MC_RED)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        self._build_header()
        self._build_form()
        self._build_footer()

    def _build_header(self):
        """McJin logo banner at the top of login."""
        header = tk.Frame(self, bg=MC_RED)
        header.pack(fill="x", pady=(40, 10))
        tk.Label(header, text="McJin", font=("Arial Black", 48, "bold"),
                 bg=MC_RED, fg=MC_YELLOW).pack()
        tk.Label(header, text="Point of Sale System",
                 font=("Arial", 14), bg=MC_RED, fg=MC_WHITE).pack()

    def _build_form(self):
        """Username / password entry fields and login button."""
        card = tk.Frame(self, bg=MC_WHITE, padx=40, pady=30)
        card.pack(pady=20, ipadx=20, ipady=10)

        tk.Label(card, text="Sign In", font=("Arial Black", 18, "bold"),
                 bg=MC_WHITE, fg=MC_DARK).grid(
                     row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(card, text="Username:", font=("Arial", 12, "bold"),
                 bg=MC_WHITE, fg=MC_DARK).grid(
                     row=1, column=0, sticky="e", padx=8, pady=8)
        self.username_var = tk.StringVar()
        u_entry = tk.Entry(card, textvariable=self.username_var,
                           font=("Arial", 12), width=22,
                           relief="solid", bd=1)
        u_entry.grid(row=1, column=1, pady=8)
        u_entry.focus()

        tk.Label(card, text="Password:", font=("Arial", 12, "bold"),
                 bg=MC_WHITE, fg=MC_DARK).grid(
                     row=2, column=0, sticky="e", padx=8, pady=8)
        self.password_var = tk.StringVar()
        p_entry = tk.Entry(card, textvariable=self.password_var,
                           show="*", font=("Arial", 12), width=22,
                           relief="solid", bd=1)
        p_entry.grid(row=2, column=1, pady=8)

        self.error_label = tk.Label(card, text="", font=("Arial", 10),
                                    bg=MC_WHITE, fg=MC_RED)
        self.error_label.grid(row=3, column=0, columnspan=2)

        make_mc_button(card, "LOG IN", self._attempt_login,
                       width=20, font_size=12).grid(
                           row=4, column=0, columnspan=2, pady=(16, 0))

        p_entry.bind("<Return>", lambda e: self._attempt_login())
        u_entry.bind("<Return>", lambda e: p_entry.focus())

    def _build_footer(self):
        """Demo account hint at the bottom."""
        tk.Label(self,
                 text="Demo accounts:  admin / admin123     cashier1 / pass1",
                 font=("Arial", 9), bg=MC_RED,
                 fg=MC_YELLOW).pack(side="bottom", pady=10)

    def _attempt_login(self):
        """Validate credentials and navigate to main menu."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            self._show_error("Please enter both username and password.")
            return
        if self.controller.login(username, password):
            self.controller.logged_in_user.set(username)
            self._clear_fields()
            self.controller.show_frame("MainMenuFrame")
        else:
            self._show_error("Invalid username or password.")
            self.password_var.set("")

    def _show_error(self, msg):
        self.error_label.config(text=msg)

    def _clear_fields(self):
        self.username_var.set("")
        self.password_var.set("")
        self.error_label.config(text="")


# =============================================================================
#  SCREEN 2 -- Main Menu (hub)
# =============================================================================

class MainMenuFrame(tk.Frame):
    """Post-login hub: username top-right, three action buttons in center."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=MC_DARK)
        self.controller = controller
        self._build_ui()

    def on_show(self):
        """Refresh username label every time this frame is raised."""
        self.user_label.config(
            text="User: " + self.controller.logged_in_user.get())

    def _build_ui(self):
        self._build_topbar()
        self._build_center()

    def _build_topbar(self):
        """Top bar: brand name left, logged-in username right."""
        topbar = tk.Frame(self, bg=MC_RED, pady=10)
        topbar.pack(fill="x")
        tk.Label(topbar, text="McJin POS",
                 font=("Arial Black", 16, "bold"),
                 bg=MC_RED, fg=MC_YELLOW).pack(side="left", padx=20)
        self.user_label = tk.Label(topbar, text="",
                                   font=("Arial", 12, "bold"),
                                   bg=MC_RED, fg=MC_WHITE)
        self.user_label.pack(side="right", padx=20)

    def _build_center(self):
        """Four menu action buttons centered on screen."""
        center = tk.Frame(self, bg=MC_DARK)
        center.pack(expand=True)

        tk.Label(center, text="Main Menu",
                 font=("Arial Black", 28, "bold"),
                 bg=MC_DARK, fg=MC_YELLOW).pack(pady=(0, 30))

        make_mc_button(center, "ORDER",
                       lambda: self.controller.show_frame("OrderFrame"),
                       width=26, font_size=14, pady=14).pack(pady=10)

        make_mc_button(center, "SHOW TOTAL SALES",
                       lambda: self.controller.show_frame("TotalSalesFrame"),
                       bg=MC_GREEN, fg=MC_WHITE,
                       width=26, font_size=14, pady=14).pack(pady=10)

        btn_out = make_mc_button(center, "LOG OUT",
                                 self._logout,
                                 bg=MC_DARK, fg=MC_RED,
                                 width=26, font_size=14, pady=14)
        btn_out.config(highlightthickness=2, highlightbackground=MC_RED)
        btn_out.pack(pady=10)

    def _logout(self):
        """Confirm then clear session and return to login."""
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.controller.logout()


# =============================================================================
#  SCREEN 3 -- Order Screen
# =============================================================================

class OrderFrame(tk.Frame):
    """
    Full ordering screen.
    Left  -- category tabs + scrollable menu grid (with item codes)
    Right -- current order, cash input, checkout
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=MC_LIGHT_BG)
        self.controller   = controller
        self.category_var = tk.StringVar(value="Burgers")
        self._build_ui()

    def on_show(self):
        self._refresh_order_panel()

    # ---- UI construction -------------------------------------------------

    def _build_ui(self):
        self._build_topbar()
        body = tk.Frame(self, bg=MC_LIGHT_BG)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)
        self._build_menu_panel(body)
        self._build_order_panel(body)

    def _build_topbar(self):
        topbar = tk.Frame(self, bg=MC_RED, pady=8)
        topbar.pack(fill="x")
        tk.Button(topbar, text="Back",
                  command=lambda: self.controller.show_frame("MainMenuFrame"),
                  bg=MC_YELLOW, fg=MC_DARK, font=("Arial", 10, "bold"),
                  relief="flat", cursor="hand2",
                  padx=10, pady=4).pack(side="left", padx=10)
        tk.Label(topbar, text="McJin -- Place Your Order",
                 font=("Arial Black", 15, "bold"),
                 bg=MC_RED, fg=MC_YELLOW).pack(side="left", padx=10)
        self.user_label_order = tk.Label(topbar, text="",
                                         font=("Arial", 11, "bold"),
                                         bg=MC_RED, fg=MC_WHITE)
        self.user_label_order.pack(side="right", padx=20)

    def _build_menu_panel(self, parent):
        """Left panel: category tabs + scrollable item grid."""
        left = tk.Frame(parent, bg=MC_LIGHT_BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self._build_category_tabs(left)

        self.items_canvas = tk.Canvas(left, bg=MC_LIGHT_BG,
                                      highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical",
                                  command=self.items_canvas.yview)
        self.items_canvas.configure(yscrollcommand=scrollbar.set)
        self.items_canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.items_frame = tk.Frame(self.items_canvas, bg=MC_LIGHT_BG)
        self.items_window = self.items_canvas.create_window(
            (0, 0), window=self.items_frame, anchor="nw")

        self.items_frame.bind("<Configure>", self._on_items_configure)
        self.items_canvas.bind("<Configure>", self._on_canvas_configure)
        self.items_canvas.bind("<MouseWheel>", self._on_mousewheel)

        self._filter_category("Burgers")   # must come after items_frame exists

    def _build_category_tabs(self, parent):
        """Row of category filter buttons above the menu grid."""
        categories = sorted({v[1] for v in MENU_ITEMS.values()})
        tab_frame = tk.Frame(parent, bg=MC_RED)
        tab_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        self._cat_buttons = {}
        for cat in categories:
            btn = tk.Button(
                tab_frame, text=cat,
                command=lambda c=cat: self._filter_category(c),
                bg=MC_RED, fg=MC_WHITE,
                activebackground=MC_YELLOW, activeforeground=MC_DARK,
                font=("Arial", 10, "bold"), relief="flat",
                cursor="hand2", padx=12, pady=6)
            btn.pack(side="left", padx=2, pady=4)
            self._cat_buttons[cat] = btn

    def _filter_category(self, category):
        """Highlight active tab and reload the menu grid."""
        self.category_var.set(category)
        for cat, btn in self._cat_buttons.items():
            btn.config(bg=MC_YELLOW if cat == category else MC_RED,
                       fg=MC_DARK   if cat == category else MC_WHITE)
        self._populate_menu_items()

    def _populate_menu_items(self):
        """
        Fill the grid with items for the active category.
        Uses sorted() (built-in #3) to display items A-Z by name.
        """
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        # sorted() -- built-in #3
        items = get_sorted_menu(self.category_var.get())

        COLS = 3
        for idx, (code, (name, _, price)) in enumerate(items):
            row, col = divmod(idx, COLS)
            card = tk.Frame(self.items_frame, bg=MC_WHITE,
                            relief="solid", bd=1)
            card.grid(row=row, column=col, padx=6, pady=6,
                      sticky="nsew", ipadx=4, ipady=4)
            self.items_frame.grid_columnconfigure(col, weight=1)

            tk.Label(card, text=code, font=("Courier", 9, "bold"),
                     bg=MC_YELLOW, fg=MC_DARK,
                     padx=4, pady=2).pack(anchor="ne", padx=4, pady=(4, 0))
            tk.Label(card, text=name, font=("Arial", 10, "bold"),
                     bg=MC_WHITE, fg=MC_DARK,
                     wraplength=120, justify="center").pack(pady=(2, 0))
            tk.Label(card, text=f"${price:.2f}",
                     font=("Arial", 11, "bold"),
                     bg=MC_WHITE, fg=MC_GREEN).pack()
            tk.Button(card, text="+ Add",
                      command=lambda c=code: self._add_item(c),
                      bg=MC_YELLOW, fg=MC_DARK, relief="flat",
                      font=("Arial", 9, "bold"), cursor="hand2",
                      padx=8, pady=3).pack(pady=(4, 6))

    def _build_order_panel(self, parent):
        """Right panel: order list, totals, cash input, checkout."""
        right = tk.Frame(parent, bg=MC_WHITE, relief="solid", bd=1)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        tk.Label(right, text="Your Order",
                 font=("Arial Black", 14, "bold"),
                 bg=MC_RED, fg=MC_YELLOW,
                 pady=8).grid(row=0, column=0, sticky="ew")

        cols = ("Item", "Qty", "Price", "Subtotal")
        self.order_tree = ttk.Treeview(right, columns=cols,
                                       show="headings", height=12)
        for col in cols:
            self.order_tree.heading(col, text=col)
        self.order_tree.column("Item",     width=130)
        self.order_tree.column("Qty",      width=40,  anchor="center")
        self.order_tree.column("Price",    width=60,  anchor="center")
        self.order_tree.column("Subtotal", width=70,  anchor="center")

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=26)
        style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"), background=MC_GRAY)
        self.order_tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)

        tk.Button(right, text="Remove Selected",
                  command=self._remove_selected,
                  bg=MC_RED, fg=MC_WHITE, relief="flat",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  pady=4).grid(row=2, column=0, sticky="ew", padx=8, pady=2)

        ttk.Separator(right, orient="horizontal").grid(
            row=3, column=0, sticky="ew", padx=8, pady=4)

        # item count label -- uses len() (built-in #1)
        self.count_label = tk.Label(right, text="Items: 0",
                                    font=("Arial", 10),
                                    bg=MC_WHITE, fg=MC_DARK)
        self.count_label.grid(row=4, column=0, padx=12, sticky="w")

        self.total_label = tk.Label(right, text="Total:  $0.00",
                                    font=("Arial Black", 14, "bold"),
                                    bg=MC_WHITE, fg=MC_DARK)
        self.total_label.grid(row=5, column=0, padx=12, pady=4, sticky="e")

        cash_frame = tk.Frame(right, bg=MC_WHITE)
        cash_frame.grid(row=6, column=0, padx=8, pady=4, sticky="ew")
        cash_frame.grid_columnconfigure(1, weight=1)
        tk.Label(cash_frame, text="Cash Tendered ($):",
                 font=("Arial", 10, "bold"),
                 bg=MC_WHITE).grid(row=0, column=0, sticky="w")
        self.cash_var = tk.StringVar()
        cash_entry = tk.Entry(cash_frame, textvariable=self.cash_var,
                              font=("Arial", 12), width=12,
                              relief="solid", bd=1, justify="right")
        cash_entry.grid(row=0, column=1, padx=(6, 0), sticky="e")

        qc_frame = tk.Frame(right, bg=MC_WHITE)
        qc_frame.grid(row=7, column=0, padx=8, pady=2, sticky="ew")
        for amt in (5, 10, 20, 50, 100):
            tk.Button(qc_frame, text=f"${amt}",
                      command=lambda a=amt: self.cash_var.set(str(a)),
                      bg=MC_GRAY, fg=MC_DARK, relief="flat",
                      font=("Arial", 9), cursor="hand2",
                      padx=6, pady=3).pack(side="left", padx=2)

        make_mc_button(right, "CHECKOUT",
                       self._checkout,
                       bg=MC_GREEN, fg=MC_WHITE,
                       width=22, font_size=12,
                       pady=10).grid(row=8, column=0,
                                     padx=8, pady=8, sticky="ew")

        make_mc_button(right, "CLEAR ORDER",
                       self._clear_order,
                       bg=MC_RED, fg=MC_WHITE,
                       width=22, font_size=11,
                       pady=6).grid(row=9, column=0,
                                    padx=8, pady=4, sticky="ew")

    # ---- canvas helpers --------------------------------------------------

    def _on_items_configure(self, event):
        self.items_canvas.configure(
            scrollregion=self.items_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.items_canvas.itemconfig(self.items_window, width=event.width)

    def _on_mousewheel(self, event):
        self.items_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---- order actions ---------------------------------------------------

    def _add_item(self, code):
        self.controller.add_to_order(code)
        self._refresh_order_panel()

    def _remove_selected(self):
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showinfo("Remove Item",
                                "Please select an item to remove.")
            return
        code = self.order_tree.item(selected[0], "tags")[0]
        self.controller.remove_from_order(code)
        self._refresh_order_panel()

    def _clear_order(self):
        if self.controller.current_order:
            if messagebox.askyesno("Clear Order",
                                   "Remove all items from the order?"):
                self.controller.clear_order()
                self._refresh_order_panel()

    def _refresh_order_panel(self):
        """
        Redraw order treeview and update totals.
        Uses len() (built-in #1) to show item count.
        """
        self.user_label_order.config(
            text="User: " + self.controller.logged_in_user.get())

        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        for item in self.controller.current_order:
            subtotal = item["price"] * item["qty"]
            self.order_tree.insert("", "end",
                                   values=(item["name"],
                                           item["qty"],
                                           f"${item['price']:.2f}",
                                           f"${subtotal:.2f}"),
                                   tags=(item["code"],))

        # len() -- built-in #1
        item_count = count_order_items(self.controller.current_order)
        self.count_label.config(
            text=f"Items: {item_count}  (len() counts {item_count} line(s))")

        total = self.controller.get_order_total()
        self.total_label.config(text=f"Total:  ${total:.2f}")

    def _checkout(self):
        """Validate cash and finalize the sale."""
        if not self.controller.current_order:
            messagebox.showwarning("Empty Order",
                                   "Please add items before checking out.")
            return
        try:
            cash = float(self.cash_var.get())
        except ValueError:
            messagebox.showerror("Invalid Cash",
                                 "Please enter a valid cash amount.")
            return

        total = self.controller.get_order_total()
        if cash < total:
            messagebox.showerror(
                "Insufficient Cash",
                f"Cash (${cash:.2f}) is less than total (${total:.2f}).")
            return

        total, change = self.controller.finalize_sale(cash)
        self._show_receipt(total, cash, change)
        self.cash_var.set("")
        self._refresh_order_panel()

    def _show_receipt(self, total, cash, change):
        """Pop up a formatted receipt window."""
        receipt_win = tk.Toplevel(self)
        receipt_win.title("Receipt")
        receipt_win.geometry("400x560")
        receipt_win.configure(bg=MC_WHITE)
        receipt_win.resizable(False, False)

        tk.Label(receipt_win, text="McJin",
                 font=("Arial Black", 22, "bold"),
                 bg=MC_WHITE, fg=MC_RED).pack(pady=(20, 2))
        tk.Label(receipt_win, text="Thank you for your order!",
                 font=("Arial", 10), bg=MC_WHITE, fg=MC_DARK).pack()

        ttk.Separator(receipt_win).pack(fill="x", padx=20, pady=10)

        last = self.controller.sales_log[-1]
        items_frame = tk.Frame(receipt_win, bg=MC_WHITE)
        items_frame.pack(fill="x", padx=24)

        tk.Label(items_frame,
                 text=f"{'Item':<25}{'Qty':>3}{'Amount':>10}",
                 font=("Courier", 9, "bold"),
                 bg=MC_WHITE).pack(anchor="w")

        for item in last["items"]:
            sub = item["price"] * item["qty"]
            tk.Label(items_frame,
                     text=f"{item['name'][:24]:<25}{item['qty']:>3}  ${sub:>6.2f}",
                     font=("Courier", 9),
                     bg=MC_WHITE).pack(anchor="w")

        ttk.Separator(receipt_win).pack(fill="x", padx=20, pady=10)

        totals_frame = tk.Frame(receipt_win, bg=MC_WHITE)
        totals_frame.pack(padx=24, fill="x")

        def receipt_row(label, value, bold=False):
            f = ("Arial Black", 11) if bold else ("Arial", 11)
            row = tk.Frame(totals_frame, bg=MC_WHITE)
            row.pack(fill="x")
            tk.Label(row, text=label, font=f,
                     bg=MC_WHITE).pack(side="left")
            tk.Label(row, text=value, font=f,
                     bg=MC_WHITE).pack(side="right")

        receipt_row("Total:",  f"${total:.2f}", bold=True)
        receipt_row("Cash:",   f"${cash:.2f}")
        # round() -- built-in #4 applied in finalize_sale
        receipt_row("Change:", f"${change:.2f}  (rounded via round())",
                    bold=True)

        tk.Label(receipt_win, text=last["timestamp"],
                 font=("Arial", 8), bg=MC_WHITE,
                 fg="gray").pack(pady=(14, 0))

        ttk.Separator(receipt_win).pack(fill="x", padx=20, pady=8)
        make_mc_button(receipt_win, "Close", receipt_win.destroy,
                       width=16, font_size=11).pack(pady=8)


# =============================================================================
#  SCREEN 4 -- Total Sales
# =============================================================================

class TotalSalesFrame(tk.Frame):
    """
    All recorded transactions with per-transaction totals and grand total.
    Uses sum() (built-in #2) and max() (built-in #5).
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=MC_DARK)
        self.controller = controller
        self._build_ui()

    def on_show(self):
        self._refresh_sales()

    def _build_ui(self):
        self._build_topbar()
        self._build_table()
        self._build_footer()

    def _build_topbar(self):
        topbar = tk.Frame(self, bg=MC_RED, pady=8)
        topbar.pack(fill="x")
        tk.Button(topbar, text="Back",
                  command=lambda: self.controller.show_frame("MainMenuFrame"),
                  bg=MC_YELLOW, fg=MC_DARK,
                  font=("Arial", 10, "bold"), relief="flat",
                  cursor="hand2", padx=10, pady=4).pack(side="left", padx=10)
        tk.Label(topbar, text="Total Sales Report",
                 font=("Arial Black", 15, "bold"),
                 bg=MC_RED, fg=MC_YELLOW).pack(side="left", padx=10)

    def _build_table(self):
        """Treeview listing every transaction."""
        table_frame = tk.Frame(self, bg=MC_DARK)
        table_frame.pack(fill="both", expand=True, padx=16, pady=10)

        cols = ("#", "Cashier", "Timestamp", "Items", "Total")
        self.sales_tree = ttk.Treeview(table_frame, columns=cols,
                                       show="headings")
        for col in cols:
            self.sales_tree.heading(col, text=col)
        self.sales_tree.column("#",         width=40,  anchor="center")
        self.sales_tree.column("Cashier",   width=100, anchor="center")
        self.sales_tree.column("Timestamp", width=160, anchor="center")
        self.sales_tree.column("Items",     width=400)
        self.sales_tree.column("Total",     width=90,  anchor="center")

        yscroll = ttk.Scrollbar(table_frame, orient="vertical",
                                command=self.sales_tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal",
                                command=self.sales_tree.xview)
        self.sales_tree.configure(yscrollcommand=yscroll.set,
                                   xscrollcommand=xscroll.set)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")
        self.sales_tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=26)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.sales_tree.bind("<<TreeviewSelect>>",
                             self._show_transaction_detail)

    def _build_footer(self):
        footer = tk.Frame(self, bg=MC_DARK, pady=12)
        footer.pack(fill="x", padx=16)

        self.tx_count_label = tk.Label(footer, text="Transactions: 0",
                                       font=("Arial", 11),
                                       bg=MC_DARK, fg=MC_WHITE)
        self.tx_count_label.pack(side="left")

        self.highest_label = tk.Label(footer, text="",
                                      font=("Arial", 10),
                                      bg=MC_DARK, fg=MC_YELLOW)
        self.highest_label.pack(side="left", padx=20)

        self.grand_label = tk.Label(footer, text="Grand Total:  $0.00",
                                    font=("Arial Black", 16, "bold"),
                                    bg=MC_DARK, fg=MC_YELLOW)
        self.grand_label.pack(side="right", padx=20)

    def _refresh_sales(self):
        """
        Reload treeview from sales_log.
        Uses sum() (built-in #2) for grand total.
        Uses max() (built-in #5) for highest sale.
        """
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        for idx, record in enumerate(self.controller.sales_log, start=1):
            items_str = ", ".join(
                f"{i['name']} x{i['qty']}" for i in record["items"])
            self.sales_tree.insert("", "end",
                                   values=(idx,
                                           record["cashier"],
                                           record["timestamp"],
                                           items_str,
                                           f"${record['total']:.2f}"),
                                   tags=(str(idx - 1),))

        # sum() -- built-in #2
        grand = compute_grand_total(self.controller.sales_log)
        self.grand_label.config(text=f"Grand Total:  ${grand:.2f}  (sum())")

        self.tx_count_label.config(
            text=f"Transactions: {len(self.controller.sales_log)}")

        # max() -- built-in #5
        best = get_highest_sale(self.controller.sales_log)
        if best:
            self.highest_label.config(
                text=f"Highest Sale: ${best['total']:.2f} "
                     f"by {best['cashier']}  (max())")
        else:
            self.highest_label.config(text="")

    def _show_transaction_detail(self, event):
        """Open a detail popup for the selected transaction row."""
        selected = self.sales_tree.selection()
        if not selected:
            return
        idx = int(self.sales_tree.item(selected[0], "tags")[0])
        if idx >= len(self.controller.sales_log):
            return
        record = self.controller.sales_log[idx]

        win = tk.Toplevel(self)
        win.title(f"Transaction #{idx + 1} Detail")
        win.geometry("420x420")
        win.configure(bg=MC_WHITE)
        win.resizable(False, False)

        tk.Label(win, text=f"Transaction #{idx + 1}",
                 font=("Arial Black", 14, "bold"),
                 bg=MC_WHITE, fg=MC_RED).pack(pady=(16, 2))
        tk.Label(win, text=record["timestamp"],
                 font=("Arial", 10), bg=MC_WHITE, fg="gray").pack()
        tk.Label(win, text=f"Cashier: {record['cashier']}",
                 font=("Arial", 10, "bold"),
                 bg=MC_WHITE).pack(pady=(4, 8))

        ttk.Separator(win).pack(fill="x", padx=20)

        list_frame = tk.Frame(win, bg=MC_WHITE)
        list_frame.pack(fill="x", padx=24, pady=8)

        tk.Label(list_frame,
                 text=f"{'Item':<26}{'Qty':>3}{'Price':>8}{'Sub':>10}",
                 font=("Courier", 9, "bold"),
                 bg=MC_WHITE).pack(anchor="w")

        for item in record["items"]:
            sub = item["price"] * item["qty"]
            tk.Label(list_frame,
                     text=(f"{item['name'][:25]:<26}"
                           f"{item['qty']:>3}"
                           f"  ${item['price']:>5.2f}"
                           f"  ${sub:>6.2f}"),
                     font=("Courier", 9),
                     bg=MC_WHITE).pack(anchor="w")

        ttk.Separator(win).pack(fill="x", padx=20, pady=6)

        totals = tk.Frame(win, bg=MC_WHITE)
        totals.pack(padx=24, fill="x")

        def row(lbl, val):
            f = tk.Frame(totals, bg=MC_WHITE)
            f.pack(fill="x")
            tk.Label(f, text=lbl, font=("Arial", 11),
                     bg=MC_WHITE).pack(side="left")
            tk.Label(f, text=val, font=("Arial", 11, "bold"),
                     bg=MC_WHITE).pack(side="right")

        row("Total:",  f"${record['total']:.2f}")
        row("Cash:",   f"${record['cash']:.2f}")
        row("Change:", f"${record['change']:.2f}")

        make_mc_button(win, "Close", win.destroy,
                       width=14, font_size=10).pack(pady=14)


# =============================================================================
#  ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    app = McJinPOS()
    app.mainloop()
