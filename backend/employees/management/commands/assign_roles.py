from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

from employees.models import Employee, EmployeeProfile


class Command(BaseCommand):

    help = "Assign roles and link employees with users"

    def handle(self, *args, **kwargs):

        # Create groups if not exists
        admin_group, _ = Group.objects.get_or_create(
            name="ADMIN"
        )

        hr_group, _ = Group.objects.get_or_create(
            name="HR"
        )

        employee_group, _ = Group.objects.get_or_create(
            name="EMPLOYEE"
        )

        # Get all employees
        employees = Employee.objects.all()

        if not employees.exists():

            self.stdout.write(
                self.style.WARNING(
                    "No employees found"
                )
            )

            return

        for emp in employees:

            try:

                # Generate username from employee email
                username = emp.email.split("@")[0]

                # Find matching Django user
                user = User.objects.filter(
                    username=username
                ).first()

                if not user:

                    self.stdout.write(
                        self.style.WARNING(
                            f"No user found for {emp.name} ({username})"
                        )
                    )

                    continue

                # Create or update employee profile
                EmployeeProfile.objects.update_or_create(

                    employee=emp,

                    defaults={
                        "user": user
                    }
                )

                # Clear previous groups
                user.groups.clear()

                dept = (
                    emp.department.strip().upper()
                    if emp.department
                    else ""
                )

                # Assign groups based on department
                if dept == "HR":

                    user.groups.add(hr_group)
                    user.is_staff = True
                    user.is_superuser = False

                elif dept == "ADMIN":

                    user.groups.add(admin_group)
                    user.is_staff = True
                    user.is_superuser = True

                else:

                    user.groups.add(employee_group)
                    user.is_staff = False
                    user.is_superuser = False

                user.save()

                self.stdout.write(

                    self.style.SUCCESS(
                        f"Role assigned to {emp.name} ({dept})"
                    )
                )

            except Exception as e:

                self.stdout.write(

                    self.style.ERROR(
                        f"Error processing {emp.name}: {e}"
                    )
                )

        self.stdout.write(

            self.style.SUCCESS(
                "All roles assigned successfully!"
            )
        )