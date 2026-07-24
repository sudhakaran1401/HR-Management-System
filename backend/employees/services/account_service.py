from django.contrib.auth.models import User, Group
from employees.models import EmployeeProfile


class AccountService:

    @staticmethod
    def generate_username(email):
        base = email.split("@")[0].lower()
        username = base
        count = 1

        while User.objects.filter(username=username).exists():
            username = f"{base}{count}"
            count += 1

        return username

    @staticmethod
    def generate_password(employee):
        first_name = employee.name.strip().split()[0].title()
        return f"{first_name}@123"

    @staticmethod
    def assign_group(user, employee):

        dept = (employee.department or "").strip().upper()

        if dept == "HR":
            group_name = "HR"

        elif dept == "ADMIN":
            group_name = "ADMIN"

        else:
            group_name = "EMPLOYEE"

        group, _ = Group.objects.get_or_create(name=group_name)

        user.groups.clear()
        user.groups.add(group)

        if group_name == "ADMIN":
            user.is_staff = True
            user.is_superuser = True

        elif group_name == "HR":
            user.is_staff = True
            user.is_superuser = False

        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()

    @staticmethod
    def create_account(employee):

        if employee.user:
            return employee.user

        username = AccountService.generate_username(employee.email)

        password = AccountService.generate_password(employee)

        user = User.objects.create_user(
            username=username,
            email=employee.email,
            password=password,
            is_active=True,
        )

        employee.user = user
        employee.save(update_fields=["user"])

        EmployeeProfile.objects.update_or_create(
            employee=employee,
            defaults={
                "user": user,
            },
        )

        AccountService.assign_group(
            user,
            employee,
        )

        return user