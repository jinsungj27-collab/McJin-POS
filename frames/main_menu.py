import tkinter as tk
from tkinter import messagebox

from config import (
    BG, SURFACE, SIDEBAR, PRIMARY, SUCCESS, TEXT, TEXT_MUTED,
    BORDER, FONT, font
)
from widgets import ModernButton, build_topbar


class MainMenuFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build_ui()

    def on_show(self):
        self.user_label.config(
            text="👤  " + self.controller.logged_in_user.get())

    def _build_ui(self):
        self.user_label = build_topbar(self, self.controller, "McJin POS")
        self._build_center()

    def _build_center(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True)

        center = tk.Frame(wrap, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="What would you like to do?",
                 font=font(24, "bold"), bg=BG,
                 fg=TEXT).pack(pady=(0, 6))
        tk.Label(center, text="Choose an option below to get started",
                 font=font(12), bg=BG,
                 fg=TEXT_MUTED).pack(pady=(0, 32))

        cards = tk.Frame(center, bg=BG)
        cards.pack()

        self._menu_card(cards, "🛒", "New Order",
                        "Take a customer order", PRIMARY,
                        lambda: self.controller.show_frame("OrderFrame"),
                        col=0)
        self._menu_card(cards, "📊", "Total Sales",
                        "View sales & reports", SUCCESS,
                        lambda: self.controller.show_frame("TotalSalesFrame"),
                        col=1)
        self._menu_card(cards, "🚪", "Log Out",
                        "End your shift", SIDEBAR,
                        self._logout, col=2)

    def _menu_card(self, parent, icon, title, subtitle, accent,
                   command, col):
        card = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER,
                        highlightthickness=1, cursor="hand2",
                        width=240, height=220)
        card.grid(row=0, column=col, padx=14)
        card.grid_propagate(False)

        strip = tk.Frame(card, bg=accent, height=6)
        strip.pack(fill="x")

        body = tk.Frame(card, bg=SURFACE)
        body.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(body, text=icon, font=(FONT, 46),
                 bg=SURFACE).pack(pady=(8, 6))
        tk.Label(body, text=title, font=font(16, "bold"),
                 bg=SURFACE, fg=TEXT).pack()
        tk.Label(body, text=subtitle, font=font(10),
                 bg=SURFACE, fg=TEXT_MUTED).pack(pady=(2, 0))

        def on_enter(_):
            card.config(highlightbackground=accent, highlightthickness=2)
        def on_leave(_):
            card.config(highlightbackground=BORDER, highlightthickness=1)

        for w in (card, strip, body, *body.winfo_children()):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", lambda e: command())

    def _logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.controller.logout()
