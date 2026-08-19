from django.db.models import Q
from employees.models import Employee


class EmployeeSelector:

    @staticmethod
    def employee_list_query(search=None):

        qs = (
            Employee.objects
            .only(
                "id",
                "name",
                "email",
                "phone",
                "department",
                "designation",
                "joining_date",
            )
            .order_by("name")
        )

        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search)
            )

        return qs