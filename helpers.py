import os
import json
from datetime import datetime

from config import SALES_FILE, MENU_ITEMS


def count_order_items(order_list):
    return len(order_list)


def compute_grand_total(sales_log):
    return sum(record["total"] for record in sales_log)


def get_sorted_menu(category):
    items = [(code, data) for code, data in MENU_ITEMS.items()
             if data[1] == category]
    return sorted(items, key=lambda x: x[1][0])


def compute_change(cash, total):
    return round(cash - total, 2)


def get_highest_sale(sales_log):
    if not sales_log:
        return None
    return max(sales_log, key=lambda r: r["total"])


def load_sales():
    if not os.path.exists(SALES_FILE):
        return []
    try:
        with open(SALES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_sales(sales_log):
    try:
        with open(SALES_FILE, "w", encoding="utf-8") as f:
            json.dump(sales_log, f, indent=2)
    except OSError:
        pass


def record_date(record):
    return record.get("date") or record["timestamp"].split(" ")[0]


def record_time(record):
    ts = record["timestamp"]
    return ts.split(" ")[1] if " " in ts else ""


def friendly_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return date_str
    if d == datetime.now().date():
        return "Today  ·  " + d.strftime("%B %d, %Y")
    return d.strftime("%A, %B %d, %Y")


def group_sales_by_day(sales_log):
    groups = {}
    for idx, rec in enumerate(sales_log):
        groups.setdefault(record_date(rec), []).append((idx, rec))
    return groups
