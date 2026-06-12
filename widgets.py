import tkinter as tk

from config import (
    BG, SURFACE, SIDEBAR, PRIMARY, PRIMARY_DK, ACCENT, ACCENT_DK,
    SUCCESS, SUCCESS_DK, DANGER, DANGER_DK, TEXT, TEXT_MUTED, TEXT_LIGHT,
    BORDER, FIELD_BG, font
)


class ModernButton(tk.Button):

    STYLES = {
        "primary": (PRIMARY, PRIMARY_DK, TEXT_LIGHT),
        "accent":  (ACCENT, ACCENT_DK, TEXT),
        "success": (SUCCESS, SUCCESS_DK, TEXT_LIGHT),
        "danger":  (DANGER, DANGER_DK, TEXT_LIGHT),
        "dark":    (SIDEBAR, "#000000", TEXT_LIGHT),
        "ghost":   (SURFACE, "#EFEFEF", TEXT),
    }

    def __init__(self, parent, text, command, kind="primary",
                 font_size=12, pad_x=18, pad_y=10, **kw):
        bg, hover, fg = self.STYLES.get(kind, self.STYLES["primary"])
        self._bg = bg
        self._hover = hover
        super().__init__(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            font=font(font_size, "bold"), relief="flat", bd=0,
            cursor="hand2", padx=pad_x, pady=pad_y,
            highlightthickness=0, **kw
        )
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


class ModernEntry(tk.Frame):

    def __init__(self, parent, textvariable=None, show=None,
                 width=24, justify="left"):
        super().__init__(parent, bg=BORDER, padx=1, pady=1)
        self.entry = tk.Entry(
            self, textvariable=textvariable, show=show,
            font=font(13), width=width, relief="flat", bd=0,
            bg=SURFACE, fg=TEXT, insertbackground=TEXT,
            justify=justify, highlightthickness=0
        )
        self.entry.pack(ipady=8, ipadx=8, fill="both", expand=True)
        self.entry.bind("<FocusIn>",
                        lambda e: self.config(bg=PRIMARY))
        self.entry.bind("<FocusOut>",
                        lambda e: self.config(bg=BORDER))

    def bind_key(self, seq, fn):
        self.entry.bind(seq, fn)

    def focus(self):
        self.entry.focus()


def build_topbar(parent, controller, title, show_back=False,
                 show_user=True):
    bar = tk.Frame(parent, bg=SIDEBAR, height=64)
    bar.pack(fill="x")
    bar.pack_propagate(False)

    left = tk.Frame(bar, bg=SIDEBAR)
    left.pack(side="left", fill="y", padx=18)

    if show_back:
        ModernButton(left, "←  Back",
                     lambda: controller.show_frame("MainMenuFrame"),
                     kind="dark", font_size=11,
                     pad_x=12, pad_y=6).pack(side="left", pady=14)

    tk.Label(left, text=title, font=font(16, "bold"),
             bg=SIDEBAR, fg=TEXT_LIGHT).pack(side="left", padx=(14, 0))

    if show_user:
        right = tk.Frame(bar, bg=SIDEBAR)
        right.pack(side="right", fill="y", padx=18)
        chip = tk.Frame(right, bg="#262932")
        chip.pack(side="right", pady=14)
        user_label = tk.Label(chip, text="", font=font(11, "bold"),
                              bg="#262932", fg=TEXT_LIGHT, padx=14, pady=6)
        user_label.pack()
        return user_label
    return None
