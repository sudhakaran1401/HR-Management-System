from decimal import Decimal

import pandas as pd

from employees.models import Employee


def get_employee(employee_id):
    employee_id = int(float(employee_id))
    return Employee.objects.get(id=employee_id)


def to_date(value):
    if pd.isna(value):
        return None
    return pd.to_datetime(value).date()


def to_decimal(value, default="0"):
    if pd.isna(value):
        return Decimal(default)
    return Decimal(str(value))


def to_int(value, default=0):
    if pd.isna(value):
        return default
    return int(float(value))


def to_string(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

def to_time(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ("", "-", "--", "N/A", "None", "nan"):
        return None

    return pd.to_datetime(value).time()