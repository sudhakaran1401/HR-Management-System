from django.core.management.base import BaseCommand
import pandas as pd

from django.contrib.auth.models import User


class Command(BaseCommand):

    help = "Import users from Excel"

    def handle(self, *args, **kwargs):

        df = pd.read_excel("employee_credentials.xlsx")

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        for _, row in df.iterrows():

            try:

                username = row["username"]
                password = row["password"]

                user, created = User.objects.get_or_create(

                    username=username
                )

                if created:

                    user.set_password(password)
                    user.save()

                    self.stdout.write(

                        self.style.SUCCESS(
                            f"User created: {username}"
                        )
                    )

                else:

                    self.stdout.write(

                        self.style.WARNING(
                            f"User already exists: {username}"
                        )
                    )

            except Exception as e:

                self.stdout.write(

                    self.style.ERROR(
                        f"Error: {e}"
                    )
                )

        self.stdout.write(

            self.style.SUCCESS(
                "User import completed!"
            )
        )