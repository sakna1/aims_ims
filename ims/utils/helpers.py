# ims/utils/helpers.py
from datetime import datetime

def parse_date(date_str, fmt="%Y-%m-%d"):
    if not date_str:
        return None
    return datetime.strptime(date_str, fmt).date()

def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
