from datetime import timedelta

import pandas as pd
from django.core.management.base import BaseCommand

from attendance.models import Attendance
from utils.excel_import import load_excel
from utils.helpers import get_employee, to_string,  to_time


class Command(BaseCommand):
    help = "Universal Attendance Import"

    def handle(self, *args, **kwargs):

        df = load_excel(
            "attendance_data.xlsx",
            required_columns=[
                "employee_id",
                "date",
                "status",
            ],
            optional_defaults={
                "check_in": None,
                "check_out": None,
                "notes": "",
            },
        )

        inserted = 0
        updated = 0
        skipped = 0

        for _, row in df.iterrows():

            try:

                employee = get_employee(row["employee_id"])

                value = str(row["date"]).strip()

                if " - " in value:
                    start, end = value.split(" - ")
                else:
                    start = end = value

                start_date = pd.to_datetime(start).date()
                end_date = pd.to_datetime(end).date()

                current = start_date

                while current <= end_date:

                    _, created = Attendance.objects.update_or_create(
                        employee=employee,
                        date=current,
                        defaults={
                            "status": to_string(row["status"]),
                            "check_in": to_time(row["check_in"]),
                            "check_out": to_time(row["check_out"]),
                            "notes": to_string(row["notes"]),
                        },
                    )

                    if created:
                        inserted += 1
                    else:
                        updated += 1

                    current += timedelta(days=1)

            except Exception as e:

                skipped += 1
                self.stdout.write(self.style.WARNING(str(e)))

        self.stdout.write(self.style.SUCCESS("Attendance Import Completed"))
        self.stdout.write(f"Inserted : {inserted}")
        self.stdout.write(f"Updated  : {updated}")
        self.stdout.write(f"Skipped  : {skipped}")