from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from payroll.services.permission_service import PermissionService
from payroll.services.report_service import ReportService

@login_required
def salary_chart_api(request):

    if not PermissionService.is_hr_or_admin(request.user):
        return HttpResponseForbidden()

    data = ReportService.get_salary_chart_data(request)

    return JsonResponse(data)