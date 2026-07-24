from django.core.management.base import BaseCommand
import pandas as pd

from django.contrib.auth.models import User

from employees.models import Employee


class Command(BaseCommand):

    help = "Import employee data"

    def handle(self, *args, **kwargs):

        df = pd.read_excel("employee_data.xlsx")

        df.columns = ( 
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        for _, row in df.iterrows():

            try:

                username = row["email"].split("@")[0]

                # Create user
                user, created = User.objects.get_or_create(

                    username=username,

                    defaults={

                        "email": row["email"],
                        "first_name": row["name"],
                    }
                )

                if created:

                    user.set_password("Employee@123")
                    user.save()

                # Create employee
                employee, created = Employee.objects.get_or_create(

                    email=row["email"],

                    defaults={

                        "name": row["name"],
                        "phone": row["phone"],
                        "designation": row["designation"],
                        "department": row["department"],
                        "joining_date": pd.to_datetime(
                            row["joining_date"]
                        ).date(),

                        # IMPORTANT
                        "user": user,
                    }
                )

                self.stdout.write(

                    self.style.SUCCESS(
                        f"Employee added: {employee.name}"
                    )
                )

            except Exception as e:

                self.stdout.write(

                    self.style.ERROR(
                        f"Error: {e}"
                    )
                )