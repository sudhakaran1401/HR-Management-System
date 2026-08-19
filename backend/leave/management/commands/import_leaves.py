import pandas as pd
from django.core.management.base import BaseCommand
from leave.models import LeaveRequest
from utils.excel_import import load_excel
from utils.helpers import ( get_employee, to_date, to_int, to_string )


class Command(BaseCommand):
    help = "Universal Leave Import"

    def handle(self, *args, **kwargs):

        df = load_excel(
            "leave_data.xlsx",
            required_columns=[
                "employee_id",
                "leave_type",
                "start_date",
                "end_date",
            ],
            optional_defaults={
                "days": None,
                "reason": "",
                "status": "Pending",
                "applied_date": pd.Timestamp.today(),
                "decided_date": None,
            },
        )

        inserted = 0
        updated = 0
        skipped = 0

        for _, row in df.iterrows():

            try:

                employee = get_employee(row["employee_id"])

                start_date = to_date(row["start_date"])
                end_date = to_date(row["end_date"])

                days = row["days"]

                if pd.isna(days):
                    days = (end_date - start_date).days + 1
                else:
                    days = to_int(days)

                _, created = LeaveRequest.objects.update_or_create(

                    employee=employee,
                    start_date=start_date,
                    end_date=end_date,

                    defaults={

                        "leave_type": to_string(row["leave_type"]),

                        "days": days,

                        "reason": to_string(row["reason"]),

                        "status": to_string(row["status"]),

                        "applied_at": (
                            pd.to_datetime(row["applied_date"])
                            if pd.notna(row["applied_date"])
                            else None
                        ),

                        "decided_at": (
                            pd.to_datetime(row["decided_date"])
                            if pd.notna(row["decided_date"])
                            else None
                        ),

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
                "Leave Import Completed"
            )
        )

        self.stdout.write(f"Inserted : {inserted}")
        self.stdout.write(f"Updated  : {updated}")
        self.stdout.write(f"Skipped  : {skipped}")