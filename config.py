import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SALES_FILE = os.path.join(BASE_DIR, "sales_data.json")

BG          = "#F4F5F7"
SURFACE     = "#FFFFFF"
SIDEBAR     = "#17191F"
PRIMARY     = "#E11D2A"
PRIMARY_DK  = "#B0151F"
ACCENT      = "#FFB81C"
ACCENT_DK   = "#E0A413"
SUCCESS     = "#16A34A"
SUCCESS_DK  = "#11833B"
DANGER      = "#DC2626"
DANGER_DK   = "#B91C1C"
TEXT        = "#1A1D21"
TEXT_MUTED  = "#6B7280"
TEXT_LIGHT  = "#FFFFFF"
BORDER      = "#E5E7EB"
FIELD_BG    = "#F3F4F6"

FONT = "Segoe UI"


def font(size, weight="normal"):
    return (FONT, size, weight)


def _load_credentials():
    raw = os.getenv("POS_CREDENTIALS", "")
    creds = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if ":" in pair:
            user, pwd = pair.split(":", 1)
            creds[user.strip()] = pwd.strip()
    return creds


CREDENTIALS = _load_credentials()

CATEGORY_ICONS = {
    "Burgers":   "🍔",
    "Chicken":   "🍗",
    "Sides":     "🍟",
    "Drinks":    "🥤",
    "Breakfast": "🍳",
    "Desserts":  "🍦",
    "Rice Meals":"🍚",
}

CURRENCY = "₱"

MENU_ITEMS = {
    "B01": ("Big Mac",                   "Burgers",   249),
    "B02": ("Quarter Pounder w/ Cheese", "Burgers",   279),
    "B03": ("McDouble",                  "Burgers",   159),
    "B04": ("McChicken",                 "Burgers",   139),
    "B05": ("Filet-O-Fish",              "Burgers",   169),
    "B06": ("Hamburger",                 "Burgers",    89),
    "B07": ("Cheeseburger",              "Burgers",   109),
    "B08": ("Double Cheeseburger",       "Burgers",   149),
    "B09": ("Bacon Deluxe",              "Burgers",   219),
    "B10": ("McJin Special",             "Burgers",   299),
    "C01": ("10pc Chicken McNuggets",    "Chicken",   249),
    "C02": ("6pc Chicken McNuggets",     "Chicken",   169),
    "C03": ("Crispy Chicken Sandwich",   "Chicken",   189),
    "C04": ("Spicy McChicken",           "Chicken",   149),
    "C05": ("2pc Fried Chicken",         "Chicken",   139),
    "C06": ("Chicken Fillet",            "Chicken",   109),
    "C07": ("Spicy Chicken Tenders (4pc)","Chicken",  179),
    "C08": ("Chicken Bucket (8pc)",      "Chicken",   499),
    "R01": ("Chicken McDo w/ Rice",      "Rice Meals",129),
    "R02": ("1pc Chicken w/ McSpaghetti","Rice Meals",169),
    "R03": ("Burger Steak w/ Rice",      "Rice Meals",109),
    "R04": ("2pc Burger Steak w/ Rice",  "Rice Meals",149),
    "R05": ("McSpaghetti w/ Chicken",    "Rice Meals",189),
    "R06": ("Crispy Chicken Fillet w/ Rice","Rice Meals",139),
    "S01": ("Large Fries",               "Sides",      99),
    "S02": ("Medium Fries",              "Sides",      69),
    "S03": ("Small Fries",               "Sides",      49),
    "S04": ("Corn on the Cob",           "Sides",      55),
    "S05": ("Side Salad",                "Sides",      89),
    "S06": ("Mashed Potato",             "Sides",      59),
    "S07": ("Coleslaw",                  "Sides",      45),
    "S08": ("Hash Browns (2pc)",         "Sides",      65),
    "D01": ("Large Coca-Cola",           "Drinks",     65),
    "D02": ("Medium Coca-Cola",          "Drinks",     49),
    "D03": ("Small Coca-Cola",           "Drinks",     35),
    "D04": ("Large Sprite",              "Drinks",     65),
    "D05": ("Iced Tea (Large)",          "Drinks",     59),
    "D06": ("Hot Coffee",                "Drinks",     49),
    "D07": ("McCafe Latte",              "Drinks",    129),
    "D08": ("McCafe Mocha Frappe",       "Drinks",    149),
    "D09": ("Chocolate Milkshake",       "Drinks",    109),
    "D10": ("Mango Pineapple Smoothie",  "Drinks",    119),
    "D11": ("Orange Juice",              "Drinks",     59),
    "D12": ("Bottled Water",             "Drinks",     29),
    "K01": ("Egg McMuffin",              "Breakfast", 109),
    "K02": ("Sausage McMuffin",          "Breakfast",  99),
    "K03": ("Big Breakfast",             "Breakfast", 199),
    "K04": ("Hotcakes (3pc)",            "Breakfast", 119),
    "K05": ("Longganisa w/ Rice & Egg",  "Breakfast", 129),
    "K06": ("Tocino w/ Rice & Egg",      "Breakfast", 129),
    "K07": ("Scrambled Eggs & Toast",    "Breakfast",  89),
    "E01": ("McFlurry Oreo",             "Desserts",  109),
    "E02": ("McFlurry Kit Kat",          "Desserts",  109),
    "E03": ("Sundae (Hot Fudge)",        "Desserts",   49),
    "E04": ("Sundae (Caramel)",          "Desserts",   49),
    "E05": ("Apple Pie",                 "Desserts",   55),
    "E06": ("Cone (Vanilla)",            "Desserts",   29),
    "E07": ("Cone (Chocolate Dip)",      "Desserts",   39),
    "E08": ("Banana Pie",                "Desserts",   45),
}
