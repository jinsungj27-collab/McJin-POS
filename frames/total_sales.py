import tkinter as tk
from tkinter import ttk, messagebox

from config import (
    BG, SURFACE, SIDEBAR, PRIMARY, ACCENT, ACCENT_DK, SUCCESS, DANGER,
    TEXT, TEXT_MUTED, TEXT_LIGHT, BORDER, FIELD_BG, MENU_ITEMS, CURRENCY, font
)
from widgets import ModernButton, ModernEntry, build_topbar
from helpers import (
    compute_grand_total, compute_change, get_highest_sale,
    save_sales, record_time, friendly_date, group_sales_by_day
)


class TotalSalesFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def on_show(self):
        self._refresh_sales()

    def _build_ui(self):
        build_topbar(self, self.controller, "Total Sales Report",
                     show_back=True, show_user=False)
        self._build_stats()
        self._build_table()

    def _build_stats(self):
        stats = tk.Frame(self, bg=BG)
        stats.pack(fill="x", padx=16, pady=(16, 8))
        for i in range(4):
            stats.grid_columnconfigure(i, weight=1, uniform="s")

        self.grand_value = self._stat_card(
            stats, 0, "💰", "Grand Total", "$0.00", SUCCESS)
        self.count_value = self._stat_card(
            stats, 1, "🧾", "Total Orders", "0", PRIMARY)
        self.days_value = self._stat_card(
            stats, 2, "📅", "Sales Days", "0", SIDEBAR)
        self.high_value = self._stat_card(
            stats, 3, "⭐", "Highest Sale", "—", ACCENT_DK)

    def _stat_card(self, parent, col, icon, label, value, accent):
        card = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER,
                        highlightthickness=1)
        card.grid(row=0, column=col, sticky="ew", padx=6)
        strip = tk.Frame(card, bg=accent, width=5)
        strip.pack(side="left", fill="y")
        body = tk.Frame(card, bg=SURFACE)
        body.pack(side="left", fill="both", expand=True, padx=16, pady=14)
        tk.Label(body, text=f"{icon}  {label}", font=font(10, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w")
        val = tk.Label(body, text=value, font=font(22, "bold"),
                       bg=SURFACE, fg=TEXT)
        val.pack(anchor="w", pady=(4, 0))
        return val

    def _build_table(self):
        table_card = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER,
                              highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=16, pady=(8, 16))

        header = tk.Frame(table_card, bg=SURFACE)
        header.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(header, text="Sales History — grouped by day",
                 font=font(13, "bold"), bg=SURFACE, fg=TEXT,
                 anchor="w").pack(side="left")
        tk.Label(header,
                 text="Right-click an order to edit/delete",
                 font=font(9), bg=SURFACE, fg=TEXT_MUTED).pack(side="right")

        table_frame = tk.Frame(table_card, bg=SURFACE)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("cashier", "time", "items", "total")
        self.sales_tree = ttk.Treeview(table_frame, columns=cols,
                                       show="tree headings")
        self.sales_tree.heading("#0", text="Date / Order")
        self.sales_tree.heading("cashier", text="Cashier")
        self.sales_tree.heading("time", text="Time")
        self.sales_tree.heading("items", text="Items")
        self.sales_tree.heading("total", text="Total")
        self.sales_tree.column("#0",      width=260, anchor="w")
        self.sales_tree.column("cashier", width=100, anchor="center")
        self.sales_tree.column("time",    width=90,  anchor="center")
        self.sales_tree.column("items",   width=360, anchor="w")
        self.sales_tree.column("total",   width=110, anchor="e")

        yscroll = ttk.Scrollbar(table_frame, orient="vertical",
                                command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")
        self.sales_tree.pack(fill="both", expand=True)
        
        def _scroll_tree(e):
            self.sales_tree.yview_scroll(int(-1 * (e.delta / 120)), "units")
        
        self.sales_tree.bind("<MouseWheel>", _scroll_tree)
        table_frame.bind("<MouseWheel>", _scroll_tree)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=font(10), rowheight=30,
                        background=SURFACE, fieldbackground=SURFACE,
                        borderwidth=0)
        style.configure("Treeview.Heading", font=font(10, "bold"),
                        background=FIELD_BG, foreground=TEXT,
                        relief="flat", padding=6)
        style.map("Treeview", background=[("selected", "#FDE7E9")],
                  foreground=[("selected", TEXT)])

        self.sales_tree.tag_configure(
            "day", background="#FDECEC", font=font(11, "bold"))
        self.sales_tree.tag_configure("order", font=font(10))

        self.sales_tree.bind("<<TreeviewSelect>>",
                             self._show_transaction_detail)
        self.sales_tree.bind("<MouseWheel>",
            lambda e: self.sales_tree.yview_scroll(
                int(-1 * (e.delta / 120)), "units"))

        self._context_menu = tk.Menu(self.sales_tree, tearoff=0,
                                     font=font(11), bg=SURFACE, fg=TEXT,
                                     activebackground=PRIMARY,
                                     activeforeground=TEXT_LIGHT)
        self._context_menu.add_command(label="✏️  Edit Transaction",
                                       command=self._edit_selected)
        self._context_menu.add_command(label="🗑️  Delete Transaction",
                                       command=self._delete_selected)
        self.sales_tree.bind("<Button-3>", self._on_right_click)

    def _refresh_sales(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        self._row_index = {}
        sales_log = self.controller.sales_log
        groups = group_sales_by_day(sales_log)

        for date in sorted(groups, reverse=True):
            recs = groups[date]
            day_total = sum(r["total"] for _, r in recs)
            parent = self.sales_tree.insert(
                "", "end",
                text=f"📅  {friendly_date(date)}",
                values=("", "", f"{len(recs)} order(s)",
                        f"{CURRENCY}{day_total:.2f}"),
                open=True, tags=("day",))

            for idx, rec in recs:
                items_str = ", ".join(
                    f"{i['name']} x{i['qty']}" for i in rec["items"])
                iid = self.sales_tree.insert(
                    parent, "end",
                    text=f"     Order #{idx + 1}",
                    values=(rec["cashier"],
                            record_time(rec),
                            items_str,
                            f"{CURRENCY}{rec['total']:.2f}"),
                    tags=("order",))
                self._row_index[iid] = idx

        grand = compute_grand_total(sales_log)
        self.grand_value.config(text=f"{CURRENCY}{grand:.2f}")
        self.count_value.config(text=str(len(sales_log)))
        self.days_value.config(text=str(len(groups)))

        best = get_highest_sale(sales_log)
        self.high_value.config(
            text=f"{CURRENCY}{best['total']:.2f}" if best else "—")

    def _show_transaction_detail(self, event):
        selected = self.sales_tree.selection()
        if not selected:
            return
        idx = self._row_index.get(selected[0])
        if idx is None:
            return
        record = self.controller.sales_log[idx]

        win = tk.Toplevel(self)
        win.title(f"Transaction #{idx + 1}")
        win.geometry("440x480")
        win.configure(bg=SURFACE)
        win.resizable(False, False)
        win.transient(self)

        head = tk.Frame(win, bg=SIDEBAR)
        head.pack(fill="x")
        tk.Label(head, text=f"Transaction #{idx + 1}",
                 font=font(16, "bold"), bg=SIDEBAR,
                 fg=TEXT_LIGHT).pack(pady=(16, 2))
        tk.Label(head, text=record["timestamp"], font=font(10),
                 bg=SIDEBAR, fg="#9AA0AB").pack()
        tk.Label(head, text=f"👤  {record['cashier']}",
                 font=font(10, "bold"), bg=SIDEBAR,
                 fg=ACCENT).pack(pady=(4, 16))

        scroll_container = tk.Frame(win, bg=SURFACE)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)

        detail_canvas = tk.Canvas(scroll_container, bg=SURFACE,
                                  highlightthickness=0)
        detail_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical",
                                         command=detail_canvas.yview)
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        detail_canvas.pack(side="left", fill="both", expand=True)
        detail_scrollbar.pack(side="right", fill="y")

        body = tk.Frame(detail_canvas, bg=SURFACE)
        body_window = detail_canvas.create_window(
            (0, 0), window=body, anchor="nw")
        
        body.bind("<Configure>",
                  lambda e: detail_canvas.configure(
                      scrollregion=detail_canvas.bbox("all")))
        detail_canvas.bind("<Configure>",
                           lambda e: detail_canvas.itemconfig(
                               body_window, width=e.width))
        detail_canvas.bind("<MouseWheel>",
                           lambda e: detail_canvas.yview_scroll(
                               int(-1 * (e.delta / 120)), "units"))

        items_frame = tk.Frame(body, bg=SURFACE)
        items_frame.pack(fill="x", padx=24, pady=(16, 0))

        for item in record["items"]:
            sub = item["price"] * item["qty"]
            r = tk.Frame(items_frame, bg=SURFACE)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=f"{item['qty']}×  {item['name']}",
                     font=font(11), bg=SURFACE, fg=TEXT,
                     anchor="w").pack(side="left")
            tk.Label(r, text=f"{CURRENCY}{sub:.2f}", font=font(11),
                     bg=SURFACE, fg=TEXT).pack(side="right")

        ttk.Separator(body, orient="horizontal").pack(fill="x", pady=12, padx=24)

        def trow(lbl, val, color=TEXT):
            r = tk.Frame(summary_frame, bg=SURFACE)
            r.pack(fill="x", pady=2)
            tk.Label(r, text=lbl, font=font(11, "bold"), bg=SURFACE,
                     fg=color).pack(side="left")
            tk.Label(r, text=val, font=font(11, "bold"), bg=SURFACE,
                     fg=color).pack(side="right")

        summary_frame = tk.Frame(body, bg=SURFACE)
        summary_frame.pack(fill="x", padx=24, pady=(0, 18))

        trow("Total", f"{CURRENCY}{record['total']:.2f}", PRIMARY)
        trow("Cash", f"{CURRENCY}{record['cash']:.2f}")
        trow("Change", f"{CURRENCY}{record['change']:.2f}", SUCCESS)

        btn_frame = tk.Frame(win, bg=SURFACE)
        btn_frame.pack(fill="x", padx=24, pady=(0, 18))
        ModernButton(btn_frame, "Close", win.destroy, kind="ghost",
                     font_size=11, pad_y=9).pack(fill="x")

    def _on_right_click(self, event):
        iid = self.sales_tree.identify_row(event.y)
        if iid and iid in self._row_index:
            self.sales_tree.selection_set(iid)
            self._context_menu.post(event.x_root, event.y_root)

    def _get_selected_index(self):
        selected = self.sales_tree.selection()
        if not selected:
            return None
        return self._row_index.get(selected[0])

    def _delete_selected(self):
        idx = self._get_selected_index()
        if idx is None:
            messagebox.showinfo("Delete", "Select an order to delete.")
            return
        if not messagebox.askyesno(
                "Delete Transaction",
                f"Permanently delete Transaction #{idx + 1}?\n"
                "This cannot be undone."):
            return
        del self.controller.sales_log[idx]
        save_sales(self.controller.sales_log)
        self._refresh_sales()

    def _edit_selected(self):
        idx = self._get_selected_index()
        if idx is None:
            messagebox.showinfo("Edit", "Select an order to edit.")
            return
        record = self.controller.sales_log[idx]
        self._open_edit_window(idx, record)

    def _open_edit_window(self, idx, record):
        win = tk.Toplevel(self)
        win.title(f"Edit Transaction #{idx + 1}")
        win.geometry("520x600")
        win.configure(bg=SURFACE)
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()

        head = tk.Frame(win, bg=PRIMARY)
        head.pack(fill="x")
        tk.Label(head, text=f"Edit Transaction #{idx + 1}",
                 font=font(16, "bold"), bg=PRIMARY,
                 fg=TEXT_LIGHT).pack(pady=(14, 12))

        body = tk.Frame(win, bg=SURFACE)
        body.pack(fill="both", expand=True, padx=24, pady=16)

        tk.Label(body, text="CASHIER", font=font(9, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w")
        cashier_var = tk.StringVar(value=record["cashier"])
        ModernEntry(body, textvariable=cashier_var, width=30).pack(
            fill="x", pady=(4, 16))

        tk.Label(body, text="ORDERED ITEMS",
                 font=font(9, "bold"), bg=SURFACE,
                 fg=TEXT_MUTED).pack(anchor="w")
        tk.Label(body, text="(× to remove · use dropdown + button to add)",
                 font=font(8), bg=SURFACE,
                 fg=TEXT_MUTED).pack(anchor="w", pady=(0, 6))

        items_copy = [dict(i) for i in record["items"]]

        items_frame = tk.Frame(body, bg=SURFACE)
        items_frame.pack(fill="both", expand=True)

        list_canvas = tk.Canvas(items_frame, bg=SURFACE,
                                highlightthickness=0, height=180)
        list_scrollbar = ttk.Scrollbar(items_frame, orient="vertical",
                                       command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=list_scrollbar.set)
        list_canvas.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")

        inner = tk.Frame(list_canvas, bg=SURFACE)
        inner_window = list_canvas.create_window(
            (0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: list_canvas.configure(
                       scrollregion=list_canvas.bbox("all")))
        list_canvas.bind("<Configure>",
                         lambda e: list_canvas.itemconfig(
                             inner_window, width=e.width))
        
        def _scroll_edit(e):
            list_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        
        list_canvas.bind("<MouseWheel>", _scroll_edit)
        inner.bind("<MouseWheel>", _scroll_edit)
        items_frame.bind("<MouseWheel>", _scroll_edit)
        list_canvas.bind("<MouseWheel>",
                         lambda e: list_canvas.yview_scroll(
                             int(-1 * (e.delta / 120)), "units"))

        def refresh_items_list():
            for w in inner.winfo_children():
                w.destroy()
            for i, item in enumerate(items_copy):
                row = tk.Frame(inner, bg=SURFACE,
                               highlightbackground=BORDER,
                               highlightthickness=1)
                row.pack(fill="x", pady=2, padx=2)
                tk.Label(row, text=f"{item['qty']}x  {item['name']}",
                         font=font(10), bg=SURFACE, fg=TEXT,
                         anchor="w").pack(side="left", padx=8, pady=6)
                tk.Label(row, text=f"{CURRENCY}{item['price'] * item['qty']:.2f}",
                         font=font(10, "bold"), bg=SURFACE, fg=TEXT
                         ).pack(side="right", padx=(0, 8), pady=6)
                tk.Button(row, text="×", font=font(10, "bold"),
                          bg=FIELD_BG, fg=DANGER, relief="flat", bd=0,
                          cursor="hand2", width=2,
                          command=lambda idx_i=i: remove_item(idx_i)
                          ).pack(side="right", padx=4, pady=4)

        def remove_item(i):
            items_copy[i]["qty"] -= 1
            if items_copy[i]["qty"] <= 0:
                items_copy.pop(i)
            refresh_items_list()

        refresh_items_list()

        add_frame = tk.Frame(body, bg=SURFACE)
        add_frame.pack(fill="x", pady=(12, 0))
        tk.Label(add_frame, text="ADD ITEM:", font=font(9, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(side="left")
        add_var = tk.StringVar()
        codes_list = sorted(MENU_ITEMS.keys())
        add_combo = ttk.Combobox(add_frame, textvariable=add_var,
                                 values=codes_list, state="readonly",
                                 width=6, font=font(10))
        add_combo.pack(side="left", padx=6)

        desc_label = tk.Label(add_frame, text="", font=font(9),
                              bg=SURFACE, fg=TEXT_MUTED)
        desc_label.pack(side="left", padx=4)

        def on_code_selected(event):
            code = add_var.get()
            if code in MENU_ITEMS:
                name, _, price = MENU_ITEMS[code]
                desc_label.config(text=f"{name} — {CURRENCY}{price:.2f}")

        add_combo.bind("<<ComboboxSelected>>", on_code_selected)

        def add_item_to_list():
            code = add_var.get()
            if code not in MENU_ITEMS:
                return
            name, _, price = MENU_ITEMS[code]
            for item in items_copy:
                if item["code"] == code:
                    item["qty"] += 1
                    refresh_items_list()
                    return
            items_copy.append({"code": code, "name": name,
                               "price": price, "qty": 1})
            refresh_items_list()

        ModernButton(add_frame, "+", add_item_to_list, kind="success",
                     font_size=10, pad_x=10, pad_y=4).pack(side="left",
                                                            padx=6)

        def save_changes():
            new_cashier = cashier_var.get().strip()
            if not new_cashier:
                messagebox.showerror("Error", "Cashier name cannot be empty.",
                                     parent=win)
                return
            if not items_copy:
                messagebox.showerror("Error",
                                     "Order must have at least one item.",
                                     parent=win)
                return
            record["cashier"] = new_cashier
            record["items"] = items_copy
            record["total"] = sum(
                i["price"] * i["qty"] for i in items_copy)
            record["change"] = compute_change(record["cash"], record["total"])
            save_sales(self.controller.sales_log)
            self._refresh_sales()
            win.destroy()
            messagebox.showinfo("Saved",
                                f"Transaction #{idx + 1} has been updated.")

        btn_frame = tk.Frame(win, bg=SURFACE)
        btn_frame.pack(fill="x", padx=24, pady=(0, 18))
        ModernButton(btn_frame, "Save Changes", save_changes,
                     kind="success", font_size=12,
                     pad_y=11).pack(fill="x", pady=(0, 6))
        ModernButton(btn_frame, "Cancel", win.destroy,
                     kind="ghost", font_size=11,
                     pad_y=8).pack(fill="x")
