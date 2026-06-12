import tkinter as tk
from datetime import datetime

from config import BG, CREDENTIALS, MENU_ITEMS
from helpers import compute_change, load_sales, save_sales, compute_grand_total
from frames import LoginFrame, MainMenuFrame, OrderFrame, TotalSalesFrame


class McJinPOS(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("McJin POS System")
        self.geometry("1180x760")
        self.minsize(1024, 680)
        self.configure(bg=BG)

        self.logged_in_user = tk.StringVar()
        self.sales_log      = load_sales()
        self.current_order  = []

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._build_frames()
        self.show_frame("LoginFrame")

    def _build_frames(self):
        for FrameClass in (LoginFrame, MainMenuFrame, OrderFrame,
                           TotalSalesFrame):
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def login(self, username, password):
        return CREDENTIALS.get(username) == password

    def logout(self):
        self.logged_in_user.set("")
        self.current_order.clear()
        self.show_frame("LoginFrame")

    def add_to_order(self, code):
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
        for item in self.current_order:
            if item["code"] == code:
                item["qty"] -= 1
                if item["qty"] <= 0:
                    self.current_order.remove(item)
                return

    def clear_order(self):
        self.current_order.clear()

    def get_order_total(self):
        return sum(i["price"] * i["qty"] for i in self.current_order)

    def finalize_sale(self, cash_tendered):
        total  = self.get_order_total()
        change = compute_change(cash_tendered, total)
        now    = datetime.now()
        record = {
            "cashier":   self.logged_in_user.get(),
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date":      now.strftime("%Y-%m-%d"),
            "items":     [dict(i) for i in self.current_order],
            "total":     total,
            "cash":      cash_tendered,
            "change":    change,
        }
        self.sales_log.append(record)
        save_sales(self.sales_log)
        self.clear_order()
        return total, change

    def get_grand_total(self):
        return compute_grand_total(self.sales_log)
