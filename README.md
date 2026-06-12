# McJin POS System

> A modern, desktop Point-of-Sale application for McJin fast food — built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Storage](https://img.shields.io/badge/Storage-JSON-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Role-Based Access](#role-based-access)
- [Menu Categories](#menu-categories)
- [Project Structure](#project-structure)
- [Built-in Functions Used](#built-in-functions-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 📖 About

McJin POS is a fully-featured desktop Point-of-Sale system designed for fast food operations. It handles order taking, cash tendering, receipt generation, and daily sales reporting — all in a clean, modern GUI. Built with Python and Tkinter, it requires no internet connection and stores all data locally in JSON.

---

## ✨ Features

- 🔐 **Role-based login** — Admin and Cashier roles with separate access levels
- 🛒 **Order screen** — Browse 59 menu items across 7 categories with card-based layout
- ➕ **Rate-limited Add buttons** — 400ms cooldown prevents accidental spam
- 🧾 **Receipt modal** — Scrollable receipt shown after every checkout
- 💰 **Philippine Peso (₱)** — All prices in PHP with realistic fast-food pricing
- � **Total Sales Report** — Sales grouped by day with expandable tree view
- ✏️ **Edit & Delete transactions** — Right-click any order in the sales report
- 💾 **Persistent storage** — Sales saved to `sales_data.json`, survive app restarts
- 🖱️ **Mouse wheel scroll** — Works in all scrollable areas (menu, cart, sales tree, modals)
- 👤 **Multi-account support** — Multiple cashier/admin accounts via `.env`
- 🎨 **Modern UI** — Segoe UI typography, McJin red & gold palette, hover effects

---

## 🛠️ Tech Stack

| Category       | Technology              |
|----------------|-------------------------|
| Language       | Python 3.8+             |
| GUI Framework  | Tkinter (built-in)      |
| Data Storage   | JSON (local file)       |
| Config / Auth  | python-dotenv + .env    |
| Package Manager| pip                     |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/jinsungj27-collab/McJin-POS.git

# Navigate to the project folder
cd McJin-POS

# Install dependencies
pip install python-dotenv
```

### Environment Setup

Create a `.env` file in the root directory (one already exists in the repo):

```env
POS_CREDENTIALS=admin:admin123:admin,cashier1:pass1:cashier,cashier2:pass2:cashier
```

Format: `username:password:role` — roles are either `admin` or `cashier`, comma-separated.

---

## 💻 Usage

```bash
python main.py
```

### Demo Accounts

| Username  | Password  | Role    |
|-----------|-----------|---------|
| admin     | admin123  | Admin   |
| cashier1  | pass1     | Cashier |
| cashier2  | pass2     | Cashier |

---

## 🔑 Role-Based Access

| Feature              | Admin | Cashier |
|----------------------|-------|---------|
| Place Orders         | ✅    | ✅      |
| View Total Sales     | ✅    | ❌      |
| Edit / Delete Sales  | ✅    | ❌      |
| Main Menu            | ✅    | ❌ (goes straight to Order screen) |

- Selecting the wrong role for your account shows an error — e.g. logging in as `cashier1` while selecting the **Admin** role is blocked.

---

## 🍔 Menu Categories

| Category    | Icon | Items |
|-------------|------|-------|
| Burgers     | 🍔   | 10    |
| Chicken     | 🍗   | 8     |
| Rice Meals  | 🍚   | 6     |
| Sides       | 🍟   | 8     |
| Drinks      | 🥤   | 12    |
| Breakfast   | 🍳   | 7     |
| Desserts    | 🍦   | 8     |

**59 items total** — prices range from ₱29 to ₱499.

---

## 📂 Project Structure

```
McJin-POS/
├── main.py              # Entry point — launches the app
├── app.py               # McJinPOS controller (auth, order logic, routing)
├── config.py            # Theme colors, fonts, credentials, menu data, roles
├── helpers.py           # Built-in wrappers, JSON persistence, date utilities
├── widgets.py           # Reusable UI components (ModernButton, ModernEntry, topbar)
├── frames/
│   ├── __init__.py      # Exports all frames
│   ├── login.py         # Role-based login screen
│   ├── main_menu.py     # Admin main menu (Order / Sales / Logout)
│   ├── order.py         # Order taking, cart, checkout, receipt
│   └── total_sales.py   # Sales report, day grouping, edit/delete
├── sales_data.json      # Persisted sales records (auto-generated)
├── .env                 # Credentials (not committed — add your own)
├── .gitignore
└── README.md
```

---

## 🧮 Built-in Functions Used

This project satisfies academic requirements for Python built-in function usage:

| Built-in  | Where Used                                      |
|-----------|-------------------------------------------------|
| `len()`   | `count_order_items()` — count items in cart     |
| `sum()`   | `compute_grand_total()` — total all sales       |
| `sorted()`| `get_sorted_menu()` — sort menu items by name   |
| `round()` | `compute_change()` — round change to 2 decimals |
| `max()`   | `get_highest_sale()` — find top transaction     |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

**jinsungj27-collab**

- GitHub: [@jinsungj27-collab](https://github.com/jinsungj27-collab)

---

<p align="center">Made with ❤️ by jinsungj27-collab</p>
