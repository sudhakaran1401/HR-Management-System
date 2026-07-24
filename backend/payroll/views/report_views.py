from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from payroll.models import SalaryHistory

@login_required
def payslip_view(request, employee_id):

    salary = get_object_or_404(
        SalaryHistory.objects.select_related("employee"), pk=employee_id
    )

    return render(request, "payroll/payslip_view.html", {"salary": salary})



