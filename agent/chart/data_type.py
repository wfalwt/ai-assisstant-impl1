import datetime
from decimal import Decimal


def is_number(value) -> bool:
    if isinstance(value, (int, float, Decimal)):
        return True
    return False


def is_date(value, key="") -> bool:
    if key != "":
        for date_field in ("date", "year", "month", "day", "hour", "minute", "second"):
            if date_field in key.lower():
                return True
    if isinstance(value, (datetime.date, datetime.datetime)):
        return True
    return False


def is_text(value) -> bool:
    if isinstance(value, str):
        return True
    return False
