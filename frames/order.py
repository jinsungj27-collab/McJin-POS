import tkinter as tk
from tkinter import ttk, messagebox

from config import (
    BG, SURFACE, PRIMARY, ACCENT, SUCCESS, DANGER, TEXT, TEXT_MUTED,
    TEXT_LIGHT, BORDER, FIELD_BG, FONT, MENU_ITEMS, CATEGORY_ICONS,
    CURRENCY, font
)
from widgets import ModernButton, ModernEntry, build_topbar
from helpers import count_order_items, get_sorted_menu


class OrderFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller   = controller
        self.category_var = tk.StringVar(value="Burgers")
        self._build_ui()

    def on_show(self):
        self._refresh_order_panel()

    def _build_ui(self):
        self.user_label_order = build_topbar(
            self, self.controller, "Place Your Order", show_back=True)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=16)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)
        self._build_menu_panel(body)
        self._build_order_panel(body)

    def _build_menu_panel(self, parent):
        left = tk.Frame(parent, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self._build_category_tabs(left)

        canvas_wrap = tk.Frame(left, bg=SURFACE, highlightbackground=BORDER,
                               highlightthickness=1)
        canvas_wrap.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        canvas_wrap.grid_rowconfigure(0, weight=1)
        canvas_wrap.grid_columnconfigure(0, weight=1)

        self.items_canvas = tk.Canvas(canvas_wrap, bg=SURFACE,
                                      highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_wrap, orient="vertical",
                                  command=self.items_canvas.yview)
        self.items_canvas.configure(yscrollcommand=scrollbar.set)
        self.items_canvas.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.items_frame = tk.Frame(self.items_canvas, bg=SURFACE)
        self.items_window = self.items_canvas.create_window(
            (0, 0), window=self.items_frame, anchor="nw")

        self.items_frame.bind("<Configure>", self._on_items_configure)
        self.items_canvas.bind("<Configure>", self._on_canvas_configure)
        self.items_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.items_frame.bind("<MouseWheel>", self._on_mousewheel)
        canvas_wrap.bind("<MouseWheel>", self._on_mousewheel)

        self._filter_category("Burgers")

    def _build_category_tabs(self, parent):
        categories = sorted({v[1] for v in MENU_ITEMS.values()})
        tab_frame = tk.Frame(parent, bg=BG)
        tab_frame.grid(row=0, column=0, sticky="ew")
        self._cat_buttons = {}
        for cat in categories:
            icon = CATEGORY_ICONS.get(cat, "")
            btn = tk.Button(
                tab_frame, text=f"{icon}  {cat}",
                command=lambda c=cat: self._filter_category(c),
                bg=SURFACE, fg=TEXT,
                activebackground=PRIMARY, activeforeground=TEXT_LIGHT,
                font=font(11, "bold"), relief="flat", bd=0,
                cursor="hand2", padx=14, pady=9, highlightthickness=0)
            btn.pack(side="left", padx=(0, 8))
            self._cat_buttons[cat] = btn

    def _filter_category(self, category):
        self.category_var.set(category)
        for cat, btn in self._cat_buttons.items():
            if cat == category:
                btn.config(bg=PRIMARY, fg=TEXT_LIGHT)
            else:
                btn.config(bg=SURFACE, fg=TEXT)
        self._populate_menu_items()

    def _populate_menu_items(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        items = get_sorted_menu(self.category_var.get())
        icon = CATEGORY_ICONS.get(self.category_var.get(), "🍴")

        COLS = 3
        for idx, (code, (name, _, price)) in enumerate(items):
            row, col = divmod(idx, COLS)
            self.items_frame.grid_columnconfigure(col, weight=1, uniform="m")
            self.items_frame.grid_rowconfigure(row, weight=0)

            card = tk.Frame(self.items_frame, bg=SURFACE,
                            highlightbackground=BORDER, highlightthickness=1,
                            height=200)
            card.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
            card.pack_propagate(False)

            top = tk.Frame(card, bg=SURFACE)
            top.pack(fill="x", padx=10, pady=(10, 0))
            tk.Label(top, text=code, font=("Consolas", 8, "bold"),
                     bg=FIELD_BG, fg=TEXT_MUTED,
                     padx=6, pady=2).pack(side="right")

            tk.Label(card, text=icon, font=(FONT, 28),
                     bg=SURFACE).pack(pady=(4, 2))
            tk.Label(card, text=name, font=font(10, "bold"),
                     bg=SURFACE, fg=TEXT,
                     wraplength=130, justify="center",
                     height=2).pack(padx=8)
            tk.Label(card, text=f"{CURRENCY}{price:.2f}",
                     font=font(12, "bold"),
                     bg=SURFACE, fg=SUCCESS).pack(pady=(2, 0))

            spacer = tk.Frame(card, bg=SURFACE)
            spacer.pack(fill="both", expand=True)

            add_btn = ModernButton(card, "+ Add", None, kind="accent",
                                   font_size=10, pad_y=7)
            add_btn.config(command=lambda c=code: self._add_item(c))
            add_btn.pack(fill="x", padx=10, pady=(0, 10), side="bottom")

            def make_hover(c):
                def enter(_): c.config(highlightbackground=PRIMARY,
                                       highlightthickness=2)
                def leave(_): c.config(highlightbackground=BORDER,
                                       highlightthickness=1)
                return enter, leave
            enter, leave = make_hover(card)
            card.bind("<Enter>", enter)
            card.bind("<Leave>", leave)

    def _build_order_panel(self, parent):
        right = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER,
                         highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        head = tk.Frame(right, bg=SURFACE)
        head.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 8))
        tk.Label(head, text="🧾  Current Order", font=font(15, "bold"),
                 bg=SURFACE, fg=TEXT).pack(side="left")
        self.count_label = tk.Label(head, text="0 items", font=font(10),
                                    bg=FIELD_BG, fg=TEXT_MUTED,
                                    padx=10, pady=3)
        self.count_label.pack(side="right")

        order_container = tk.Frame(right, bg=SURFACE)
        order_container.grid(row=1, column=0, sticky="nsew", padx=12)
        order_container.grid_rowconfigure(0, weight=1)
        order_container.grid_columnconfigure(0, weight=1)

        self.order_canvas = tk.Canvas(order_container, bg=SURFACE,
                                      highlightthickness=0)
        order_scrollbar = ttk.Scrollbar(order_container, orient="vertical",
                                        command=self.order_canvas.yview)
        self.order_canvas.configure(yscrollcommand=order_scrollbar.set)
        self.order_canvas.grid(row=0, column=0, sticky="nsew")
        order_scrollbar.grid(row=0, column=1, sticky="ns")

        self.order_list_frame = tk.Frame(self.order_canvas, bg=SURFACE)
        self.order_list_window = self.order_canvas.create_window(
            (0, 0), window=self.order_list_frame, anchor="nw")

        self.order_list_frame.bind("<Configure>",
            lambda e: self.order_canvas.configure(
                scrollregion=self.order_canvas.bbox("all")))
        self.order_canvas.bind("<Configure>",
            lambda e: self.order_canvas.itemconfig(
                self.order_list_window, width=e.width))
        
        def _scroll_order(e):
            self.order_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        
        self.order_canvas.bind("<MouseWheel>", _scroll_order)
        self.order_list_frame.bind("<MouseWheel>", _scroll_order)
        order_container.bind("<MouseWheel>", _scroll_order)

        summary = tk.Frame(right, bg=FIELD_BG)
        summary.grid(row=2, column=0, sticky="ew")
        inner = tk.Frame(summary, bg=FIELD_BG)
        inner.pack(fill="x", padx=18, pady=14)

        total_row = tk.Frame(inner, bg=FIELD_BG)
        total_row.pack(fill="x", pady=(0, 10))
        tk.Label(total_row, text="Total", font=font(14, "bold"),
                 bg=FIELD_BG, fg=TEXT).pack(side="left")
        self.total_label = tk.Label(total_row, text=f"{CURRENCY}0.00",
                                    font=font(20, "bold"),
                                    bg=FIELD_BG, fg=PRIMARY)
        self.total_label.pack(side="right")

        tk.Label(inner, text="CASH TENDERED", font=font(9, "bold"),
                 bg=FIELD_BG, fg=TEXT_MUTED).pack(anchor="w")
        self.cash_var = tk.StringVar()
        cash_entry = ModernEntry(inner, textvariable=self.cash_var,
                                 width=20, justify="right")
        cash_entry.pack(fill="x", pady=(4, 8))

        qc_frame = tk.Frame(inner, bg=FIELD_BG)
        qc_frame.pack(fill="x", pady=(0, 12))
        for amt in (50, 100, 200, 500, 1000):
            tk.Button(qc_frame, text=f"{CURRENCY}{amt}",
                      command=lambda a=amt: self.cash_var.set(str(a)),
                      bg=SURFACE, fg=TEXT, relief="flat", bd=0,
                      activebackground=ACCENT, activeforeground=TEXT,
                      font=font(10, "bold"), cursor="hand2",
                      padx=10, pady=6, highlightthickness=0
                      ).pack(side="left", expand=True, fill="x", padx=2)

        ModernButton(inner, "✓  Checkout", self._checkout,
                     kind="success", font_size=13,
                     pad_y=13).pack(fill="x", pady=(0, 8))
        ModernButton(inner, "Clear Order", self._clear_order,
                     kind="ghost", font_size=11,
                     pad_y=8).pack(fill="x")

    def _on_items_configure(self, event):
        self.items_canvas.configure(
            scrollregion=self.items_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.items_canvas.itemconfig(self.items_window, width=event.width)

    def _on_mousewheel(self, event):
        self.items_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _add_item(self, code):
        self.controller.add_to_order(code)
        self._refresh_order_panel()

    def _increment_item(self, code):
        self.controller.add_to_order(code)
        self._refresh_order_panel()

    def _decrement_item(self, code):
        self.controller.remove_from_order(code)
        self._refresh_order_panel()

    def _clear_order(self):
        if self.controller.current_order:
            if messagebox.askyesno("Clear Order",
                                   "Remove all items from the order?"):
                self.controller.clear_order()
                self._refresh_order_panel()

    def _refresh_order_panel(self):
        self.user_label_order.config(
            text="👤  " + self.controller.logged_in_user.get())

        for widget in self.order_list_frame.winfo_children():
            widget.destroy()

        if not self.controller.current_order:
            empty = tk.Frame(self.order_list_frame, bg=SURFACE)
            empty.pack(fill="x", pady=40)
            tk.Label(empty, text="🛒", font=(FONT, 40),
                     bg=SURFACE).pack()
            tk.Label(empty, text="Your cart is empty",
                     font=font(12, "bold"), bg=SURFACE,
                     fg=TEXT_MUTED).pack(pady=(6, 0))
            tk.Label(empty, text="Add items from the menu to begin",
                     font=font(10), bg=SURFACE,
                     fg=TEXT_MUTED).pack()
        else:
            for item in self.controller.current_order:
                self._build_order_row(item)

        item_count = count_order_items(self.controller.current_order)
        self.count_label.config(text=f"{item_count} item(s)")

        total = self.controller.get_order_total()
        self.total_label.config(text=f"{CURRENCY}{total:.2f}")

    def _build_order_row(self, item):
        subtotal = item["price"] * item["qty"]
        row = tk.Frame(self.order_list_frame, bg=SURFACE,
                       highlightbackground=BORDER, highlightthickness=1)
        row.pack(fill="x", pady=4, padx=2)

        info = tk.Frame(row, bg=SURFACE)
        info.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        tk.Label(info, text=item["name"], font=font(11, "bold"),
                 bg=SURFACE, fg=TEXT, anchor="w").pack(anchor="w")
        tk.Label(info, text=f"{CURRENCY}{item['price']:.2f} each",
                 font=font(9), bg=SURFACE, fg=TEXT_MUTED,
                 anchor="w").pack(anchor="w")

        right = tk.Frame(row, bg=SURFACE)
        right.pack(side="right", padx=10, pady=8)

        tk.Label(right, text=f"{CURRENCY}{subtotal:.2f}", font=font(11, "bold"),
                 bg=SURFACE, fg=TEXT).pack(side="right", padx=(10, 0))

        qty = tk.Frame(right, bg=SURFACE)
        qty.pack(side="right")
        tk.Button(qty, text="−", font=font(11, "bold"),
                  bg=FIELD_BG, fg=DANGER, relief="flat", bd=0,
                  width=2, cursor="hand2", activebackground="#FCE8E8",
                  command=lambda c=item["code"]: self._decrement_item(c)
                  ).pack(side="left")
        tk.Label(qty, text=str(item["qty"]), font=font(11, "bold"),
                 bg=SURFACE, fg=TEXT, width=3,
                 anchor="center").pack(side="left")
        tk.Button(qty, text="+", font=font(11, "bold"),
                  bg=FIELD_BG, fg=SUCCESS, relief="flat", bd=0,
                  width=2, cursor="hand2", activebackground="#E3F7E9",
                  command=lambda c=item["code"]: self._increment_item(c)
                  ).pack(side="left")

    def _checkout(self):
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
                f"Cash ({CURRENCY}{cash:.2f}) is less than total "
                f"({CURRENCY}{total:.2f}).")
            return

        total, change = self.controller.finalize_sale(cash)
        self._show_receipt(total, cash, change)
        self.cash_var.set("")
        self._refresh_order_panel()

    def _show_receipt(self, total, cash, change):
        win = tk.Toplevel(self)
        win.title("Receipt")
        win.geometry("400x600")
        win.configure(bg=SURFACE)
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()

        head = tk.Frame(win, bg=PRIMARY)
        head.pack(fill="x")
        tk.Label(head, text="McJin", font=font(26, "bold"),
                 bg=PRIMARY, fg=TEXT_LIGHT).pack(pady=(18, 0))
        tk.Label(head, text="Order Confirmed ✓", font=font(11),
                 bg=PRIMARY, fg=ACCENT).pack(pady=(0, 16))

        scroll_container = tk.Frame(win, bg=SURFACE)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)

        receipt_canvas = tk.Canvas(scroll_container, bg=SURFACE,
                                   highlightthickness=0)
        receipt_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical",
                                          command=receipt_canvas.yview)
        receipt_canvas.configure(yscrollcommand=receipt_scrollbar.set)
        receipt_canvas.pack(side="left", fill="both", expand=True)
        receipt_scrollbar.pack(side="right", fill="y")

        body = tk.Frame(receipt_canvas, bg=SURFACE)
        body_window = receipt_canvas.create_window(
            (0, 0), window=body, anchor="nw")
        
        body.bind("<Configure>",
                  lambda e: receipt_canvas.configure(
                      scrollregion=receipt_canvas.bbox("all")))
        receipt_canvas.bind("<Configure>",
                            lambda e: receipt_canvas.itemconfig(
                                body_window, width=e.width))
        receipt_canvas.bind("<MouseWheel>",
                            lambda e: receipt_canvas.yview_scroll(
                                int(-1 * (e.delta / 120)), "units"))

        items_frame = tk.Frame(body, bg=SURFACE)
        items_frame.pack(fill="x", padx=26, pady=(18, 0))

        last = self.controller.sales_log[-1]
        for item in last["items"]:
            sub = item["price"] * item["qty"]
            r = tk.Frame(items_frame, bg=SURFACE)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=f"{item['qty']}×  {item['name']}",
                     font=font(11), bg=SURFACE, fg=TEXT,
                     anchor="w").pack(side="left")
            tk.Label(r, text=f"{CURRENCY}{sub:.2f}", font=font(11),
                     bg=SURFACE, fg=TEXT).pack(side="right")

        ttk.Separator(body, orient="horizontal").pack(fill="x", pady=12, padx=26)

        def trow(label, value, big=False, color=TEXT):
            r = tk.Frame(summary_frame, bg=SURFACE)
            r.pack(fill="x", pady=2)
            f = font(15, "bold") if big else font(11)
            tk.Label(r, text=label, font=f, bg=SURFACE,
                     fg=color).pack(side="left")
            tk.Label(r, text=value, font=f, bg=SURFACE,
                     fg=color).pack(side="right")

        summary_frame = tk.Frame(body, bg=SURFACE)
        summary_frame.pack(fill="x", padx=26, pady=(0, 0))

        trow("Total", f"{CURRENCY}{total:.2f}", big=True, color=PRIMARY)
        trow("Cash", f"{CURRENCY}{cash:.2f}")
        trow("Change", f"{CURRENCY}{change:.2f}", big=True, color=SUCCESS)

        footer_frame = tk.Frame(body, bg=SURFACE)
        footer_frame.pack(fill="x", padx=26, pady=(16, 0))

        tk.Label(footer_frame, text=last["timestamp"], font=font(8),
                 bg=SURFACE, fg=TEXT_MUTED).pack(pady=(0, 0))
        tk.Label(footer_frame, text="Thank you for choosing McJin!",
                 font=font(10, "bold"), bg=SURFACE,
                 fg=TEXT_MUTED).pack(pady=(2, 18))

        btn_frame = tk.Frame(win, bg=SURFACE)
        btn_frame.pack(fill="x", padx=26, pady=(0, 20))
        ModernButton(btn_frame, "Close", win.destroy, kind="primary",
                     font_size=12, pad_y=11).pack(fill="x")
