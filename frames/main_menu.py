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
        role = self.controller.logged_in_role.get()
        if role == "cashier":
            self.controller.show_frame("OrderFrame")

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
        # Fixed size card — grid_propagate(False) + fixed width/height
        # prevents the card from resizing when highlight border changes
        card = tk.Frame(parent, bg=SURFACE,
                        highlightbackground=BORDER,
                        highlightthickness=2,
                        cursor="hand2",
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

        # ── Stable hover: bind only to the card frame, check pointer
        # position on leave to avoid child-widget flicker.
        def _is_inside_card():
            try:
                px, py = card.winfo_pointerxy()
                rx, ry = card.winfo_rootx(), card.winfo_rooty()
                rw, rh = card.winfo_width(), card.winfo_height()
                return rx <= px < rx + rw and ry <= py < ry + rh
            except tk.TclError:
                return False

        def on_enter(_):
            card.config(highlightbackground=accent)

        def on_leave(_):
            # Small delay so that moving to a child widget doesn't
            # fire a false leave — re-check pointer is still outside
            card.after(20, lambda: card.config(
                highlightbackground=BORDER)
                if not _is_inside_card() else None)

        # Bind only to the card container — NOT to children.
        # Children inherit cursor but don't trigger their own Enter/Leave.
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Click propagates correctly through all children
        def _click(e):
            command()

        for w in (card, strip, body, *body.winfo_children()):
            w.bind("<Button-1>", _click)

    def _logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.controller.logout()
