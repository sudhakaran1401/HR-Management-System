import os
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth.models import Group, User

from employees.models import Employee, EmployeeProfile
from leave.models import LeaveBalance, LeaveRequest
from attendance.models import Attendance
from payroll.models import SalaryHistory


HR_USERNAME = "e2e_hr"
HR_EMAIL = "e2e.hr@example.com"
HR_PASSWORD = "Test@12345"

EMP_USERNAME = "e2e_employee"
EMP_EMAIL = "e2e.employee@example.com"
EMP_PASSWORD = "Test@12345"


def upsert_user(username, email, password, group_name):
    user, _ = User.objects.get_or_create(username=username)

    user.email = email
    user.is_active = True
    user.set_password(password)

    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.set([group])

    user.is_staff = group_name in {"HR", "ADMIN"}
    user.is_superuser = group_name == "ADMIN"

    user.save()

    return user


def upsert_employee(email, name, department, designation, user):
    employee, _ = Employee.objects.get_or_create(
        email=email,
        defaults={
            "name": name,
            "phone": "9999999999",
            "department": department,
            "designation": designation,
            "joining_date": date.today(),
            "address": "E2E Test Address",
        },
    )

    employee.name = name
    employee.phone = "9999999999"
    employee.department = department
    employee.designation = designation
    employee.joining_date = date.today()
    employee.address = "E2E Test Address"
    employee.user = user

    employee.save()

    EmployeeProfile.objects.update_or_create(
        user=user,
        defaults={
            "employee": employee,
        },
    )

    return employee


def main():
    # ---------------------------------------------------------
    # USERS
    # ---------------------------------------------------------

    hr_user = upsert_user(
        HR_USERNAME,
        HR_EMAIL,
        HR_PASSWORD,
        "HR",
    )
    
    print("========== HR AUTH CHECK ==========")
    print("USERNAME:", hr_user.username)
    print("ACTIVE:", hr_user.is_active)
    print("PASSWORD VALID:", hr_user.check_password(HR_PASSWORD))
    print("GROUPS:", list(hr_user.groups.values_list("name", flat=True)))
    print("===================================")

    employee_user = upsert_user(
        EMP_USERNAME,
        EMP_EMAIL,
        EMP_PASSWORD,
        "EMPLOYEE",
    )

    # ---------------------------------------------------------
    # EMPLOYEES
    # ---------------------------------------------------------

    hr_employee = upsert_employee(
        HR_EMAIL,
        "E2E HR Manager",
        "HR",
        "HR Manager",
        hr_user,
    )

    employee = upsert_employee(
        EMP_EMAIL,
        "E2E Employee",
        "IT",
        "Software Engineer",
        employee_user,
    )

    # ---------------------------------------------------------
    # LEAVE BALANCES
    # ---------------------------------------------------------

    LeaveBalance.objects.update_or_create(
        employee=hr_employee
    )

    LeaveBalance.objects.update_or_create(
        employee=employee
    )

    # ---------------------------------------------------------
    # ATTENDANCE
    # ---------------------------------------------------------

    yesterday = date.today() - timedelta(days=1)

    Attendance.objects.update_or_create(
        employee=employee,
        date=yesterday,
        defaults={
            "status": "Present",
            "check_in": "09:00",
            "check_out": "17:30",
            "notes": "E2E seed attendance",
        },
    )

    # ---------------------------------------------------------
    # PENDING LEAVE REQUEST
    # ---------------------------------------------------------

    pending_leave, _ = LeaveRequest.objects.get_or_create(
        employee=employee,
        leave_type="CASUAL",
        start_date=date.today() + timedelta(days=10),
        end_date=date.today() + timedelta(days=11),
        defaults={
            "reason": "E2E seeded pending leave",
            "status": "PENDING",
        },
    )

    if pending_leave.status != "PENDING":
        pending_leave.status = "PENDING"
        pending_leave.save(update_fields=["status"])

    # ---------------------------------------------------------
    # SECURITY TEST LEAVE
    # ---------------------------------------------------------

    security_leave, _ = LeaveRequest.objects.get_or_create(
        employee=employee,
        leave_type="SICK",
        start_date=date.today() + timedelta(days=15),
        end_date=date.today() + timedelta(days=15),
        defaults={
            "reason": "E2E security pending leave",
            "status": "PENDING",
        },
    )

    if security_leave.status != "PENDING":
        security_leave.status = "PENDING"
        security_leave.save(update_fields=["status"])

    # ---------------------------------------------------------
    # PAYROLL
    # ---------------------------------------------------------

    pay_month = date.today().replace(day=1)

    SalaryHistory.objects.update_or_create(
        employee=employee,
        pay_month=pay_month,
        defaults={
            "amt_per_day": Decimal("100.00"),
            "notes": "E2E seed payroll",
        },
    )

    # ---------------------------------------------------------
    # VERIFICATION
    # ---------------------------------------------------------

    print("========================================")
    print("E2E seed data ready")
    print("========================================")

    print(f"HR_USERNAME={HR_USERNAME}")
    print(f"HR_PASSWORD={HR_PASSWORD}")
    print(f"EMP_USERNAME={EMP_USERNAME}")
    print(f"EMP_PASSWORD={EMP_PASSWORD}")

    print(f"HR_USER_ID={hr_user.id}")
    print(f"HR_EMPLOYEE_ID={hr_employee.id}")
    print(f"HR_EMPLOYEE_USER_ID={hr_employee.user_id}")
    print(f"HR_EMPLOYEE_DEPARTMENT={hr_employee.department}")

    print(f"EMPLOYEE_USER_ID={employee_user.id}")
    print(f"EMPLOYEE_ID={employee.id}")
    print(f"EMPLOYEE_USER_ID_LINKED={employee.user_id}")

    print(f"PENDING_LEAVE_ID={pending_leave.id}")

    print("========================================")


if __name__ == "__main__":
    main()
