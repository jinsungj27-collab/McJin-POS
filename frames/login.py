import tkinter as tk

from config import (
    BG, SURFACE, PRIMARY, ACCENT, DANGER, TEXT, TEXT_MUTED, TEXT_LIGHT,
    BORDER, FIELD_BG, FONT, font
)
from widgets import ModernButton, ModernEntry


class LoginFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
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

        pad = tk.Frame(card, bg=SURFACE, padx=44, pady=40)
        pad.pack()

        tk.Label(pad, text="Welcome back 👋",
                 font=font(22, "bold"), bg=SURFACE,
                 fg=TEXT).pack(anchor="w")
        tk.Label(pad, text="Sign in to start your shift",
                 font=font(11), bg=SURFACE,
                 fg=TEXT_MUTED).pack(anchor="w", pady=(2, 24))

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

        ModernButton(pad, "Sign In", self._attempt_login,
                     kind="primary", font_size=13,
                     pad_y=12).pack(fill="x")

        hint = tk.Frame(pad, bg=FIELD_BG)
        hint.pack(fill="x", pady=(20, 0))
        tk.Label(hint, text="Demo:  admin / admin123",
                 font=font(9), bg=FIELD_BG,
                 fg=TEXT_MUTED).pack(pady=8)

        self.p_entry.bind_key("<Return>", lambda e: self._attempt_login())
        self.u_entry.bind_key("<Return>", lambda e: self.p_entry.focus())

    def on_show(self):
        self._clear_fields()
        self.u_entry.focus()

    def _attempt_login(self):
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
