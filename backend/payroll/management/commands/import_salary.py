from decimal import Decimal

import pandas as pd
from django.core.management.base import BaseCommand

from payroll.models import SalaryHistory

from utils.excel_import import load_excel
from utils.helpers import (
    get_employee,
    to_date,
    to_decimal,
    to_string,
)


class Command(BaseCommand):
    help = "Universal Salary Import"

    def handle(self, *args, **kwargs):

        df = load_excel(
            "salary_data.xlsx",
            required_columns=[
                "employee_id",
                "pay_month",
            ],
            optional_defaults={
                "amt_per_day": None,
                "gross": None,
                "paid_date": None,
                "notes": "",
            },
        )

        inserted = 0
        updated = 0
        skipped = 0

        for _, row in df.iterrows():

            try:

                employee = get_employee(row["employee_id"])

                pay_month = to_date(row["pay_month"]).replace(day=1)

                # Determine amount per day
                if pd.notna(row["amt_per_day"]):

                    amt_per_day = to_decimal(row["amt_per_day"])

                elif pd.notna(row["gross"]):

                    amt_per_day = (
                        to_decimal(row["gross"])
                        / Decimal("30")
                    )

                else:

                    raise ValueError(
                        "Either 'Amt Per Day' or 'Gross' must be provided."
                    )

                _, created = SalaryHistory.objects.update_or_create(

                    employee=employee,
                    pay_month=pay_month,

                    defaults={

                        "amt_per_day": amt_per_day,
                        "paid_date": to_date(row["paid_date"]),
                        "notes": to_string(row["notes"]),

                    }

                )

                if created:
                    inserted += 1
                else:
                    updated += 1

            except Exception as e:

                skipped += 1
                self.stdout.write(
                    self.style.WARNING(str(e))
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Salary Import Completed"
            )
        )

        self.stdout.write(f"Inserted : {inserted}")
        self.stdout.write(f"Updated  : {updated}")
        self.stdout.write(f"Skipped  : {skipped}")