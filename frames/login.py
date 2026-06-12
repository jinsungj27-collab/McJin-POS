import tkinter as tk

from config import (
    BG, SURFACE, PRIMARY, ACCENT, DANGER, SUCCESS, TEXT, TEXT_MUTED,
    TEXT_LIGHT, BORDER, FIELD_BG, FONT, ROLES, font
)
from widgets import ModernButton, ModernEntry


class LoginFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller   = controller
        self._selected_role = tk.StringVar(value="cashier")
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1, uniform="x")
        self.grid_columnconfigure(1, weight=1, uniform="x")
        self.grid_rowconfigure(0, weight=1)
        self._build_brand_panel()
        self._build_form_panel()

    def _build_brand_panel(self):
        brand = tk.Frame(self, bg=PRIMARY)
        brand.grid(row=0, column=0, sticky="nsew")

        inner = tk.Frame(brand, bg=PRIMARY)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="🍔", font=(FONT, 72),
                 bg=PRIMARY, fg=TEXT_LIGHT).pack()
        tk.Label(inner, text="McJin", font=font(52, "bold"),
                 bg=PRIMARY, fg=TEXT_LIGHT).pack()
        tk.Label(inner, text="POINT OF SALE",
                 font=font(15, "bold"), bg=PRIMARY,
                 fg=ACCENT).pack(pady=(2, 0))
        tk.Label(inner,
                 text="Fast, friendly service\nstarts right here.",
                 font=font(13), bg=PRIMARY, fg="#FFD9DB",
                 justify="center").pack(pady=(20, 0))

    def _build_form_panel(self):
        panel = tk.Frame(self, bg=BG)
        panel.grid(row=0, column=1, sticky="nsew")

        card = tk.Frame(panel, bg=SURFACE, highlightbackground=BORDER,
                        highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        pad = tk.Frame(card, bg=SURFACE, padx=44, pady=36)
        pad.pack()

        tk.Label(pad, text="Welcome back 👋",
                 font=font(22, "bold"), bg=SURFACE,
                 fg=TEXT).pack(anchor="w")
        tk.Label(pad, text="Choose your role and sign in",
                 font=font(11), bg=SURFACE,
                 fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        # ── Role selector ──────────────────────────────────────────
        tk.Label(pad, text="SIGN IN AS", font=font(9, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))

        self.role_frame = tk.Frame(pad, bg=SURFACE)
        self.role_frame.pack(fill="x", pady=(0, 20))

        self._role_btns = {}
        for role_key, meta in ROLES.items():
            self._build_role_card(self.role_frame, role_key, meta)

        # ── Username ───────────────────────────────────────────────
        tk.Label(pad, text="USERNAME", font=font(9, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w")
        self.username_var = tk.StringVar()
        self.u_entry = ModernEntry(pad, textvariable=self.username_var,
                                   width=28)
        self.u_entry.pack(fill="x", pady=(4, 16))
        self.u_entry.focus()

        tk.Label(pad, text="PASSWORD", font=font(9, "bold"),
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w")
        self.password_var = tk.StringVar()
        self.p_entry = ModernEntry(pad, textvariable=self.password_var,
                                   show="•", width=28)
        self.p_entry.pack(fill="x", pady=(4, 8))

        self.error_label = tk.Label(pad, text="", font=font(10),
                                    bg=SURFACE, fg=DANGER)
        self.error_label.pack(anchor="w", pady=(0, 8))

        ModernButton(pad, "Sign In  →", self._attempt_login,
                     kind="primary", font_size=13,
                     pad_y=12).pack(fill="x")

        hint = tk.Frame(pad, bg=FIELD_BG)
        hint.pack(fill="x", pady=(16, 0))
        tk.Label(hint, text="Admin: admin / admin123   |   Cashier: cashier1 / pass1",
                 font=font(9), bg=FIELD_BG,
                 fg=TEXT_MUTED).pack(pady=8)

        self.p_entry.bind_key("<Return>", lambda e: self._attempt_login())
        self.u_entry.bind_key("<Return>", lambda e: self.p_entry.focus())

    def _build_role_card(self, parent, role_key, meta):
        def select(_=None):
            if self._selected_role.get() != role_key:
                self._selected_role.set(role_key)
                self._refresh_role_cards()

        card = tk.Frame(
            parent, bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=2, cursor="hand2")
        card.pack(side="left", expand=True, fill="x",
                  padx=(0, 8) if role_key == "admin" else (8, 0))

        inner = tk.Frame(card, bg=SURFACE)
        inner.pack(fill="both", padx=14, pady=12)

        icon_lbl = tk.Label(inner, text=meta["icon"], font=(FONT, 22),
                            bg=SURFACE, fg=meta["color"])
        icon_lbl.pack(anchor="w")
        title_lbl = tk.Label(inner, text=meta["label"], font=font(12, "bold"),
                            bg=SURFACE, fg=TEXT)
        title_lbl.pack(anchor="w")
        desc_lbl = tk.Label(inner, text=meta["desc"], font=font(8),
                            bg=SURFACE, fg=TEXT_MUTED,
                            wraplength=130, justify="left")
        desc_lbl.pack(anchor="w", pady=(2, 0))

        widgets = (card, inner, icon_lbl, title_lbl, desc_lbl)
        card._hovered = False

        def on_enter(_):
            card._hovered = True
            self._apply_role_style(role_key)

        def on_leave(_):
            card.after(10, _check_leave)

        def _check_leave():
            try:
                x, y = card.winfo_pointerxy()
                cx, cy = card.winfo_rootx(), card.winfo_rooty()
                cw, ch = card.winfo_width(), card.winfo_height()
                if not (cx <= x < cx + cw and cy <= y < cy + ch):
                    card._hovered = False
                    self._apply_role_style(role_key)
            except tk.TclError:
                pass

        for w in widgets:
            w.bind("<Button-1>", select)
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

        self._role_btns[role_key] = {
            "card": card, "inner": inner, "icon": icon_lbl,
            "title": title_lbl, "desc": desc_lbl, "meta": meta,
        }
        self._apply_role_style(role_key)

    def _apply_role_style(self, role_key):
        parts = self._role_btns[role_key]
        meta = parts["meta"]
        color = meta["color"]
        selected = self._selected_role.get() == role_key
        hovered = getattr(parts["card"], "_hovered", False)

        bg = color if selected else SURFACE
        parts["card"].config(bg=bg, highlightbackground=color)
        parts["inner"].config(bg=bg)
        parts["icon"].config(bg=bg,
                             fg=TEXT_LIGHT if selected else color)
        parts["title"].config(bg=bg,
                             fg=TEXT_LIGHT if selected else TEXT)
        parts["desc"].config(bg=bg,
                             fg="#FFE0B2" if selected else TEXT_MUTED)

        if not selected:
            parts["card"].config(
                highlightbackground=color if hovered else BORDER)

    def _refresh_role_cards(self):
        for role_key in self._role_btns:
            self._apply_role_style(role_key)

    def on_show(self):
        self._clear_fields()
        self._selected_role.set("cashier")
        self._refresh_role_cards()
        self.u_entry.focus()

    def _attempt_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            self._show_error("Please enter both username and password.")
            return

        if self.controller.login(username, password):
            actual_role = self.controller.logged_in_role.get()
            chosen_role = self._selected_role.get()

            if actual_role != chosen_role:
                role_label = chosen_role.capitalize()
                self._show_error(
                    f"'{username}' is not a {role_label} account.")
                self.password_var.set("")
                return

            self.controller.logged_in_user.set(username)
            self._clear_fields()
            if actual_role == "admin":
                self.controller.show_frame("MainMenuFrame")
            else:
                self.controller.show_frame("OrderFrame")
        else:
            self._show_error("Invalid username or password.")
            self.password_var.set("")

    def _show_error(self, msg):
        self.error_label.config(text=msg)

    def _clear_fields(self):
        self.username_var.set("")
        self.password_var.set("")
        self.error_label.config(text="")
