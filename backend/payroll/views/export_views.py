from django.contrib.auth.decorators import login_required
from payroll.services.export_service import ExportService
from payroll.services.payroll_pdf_service import PayrollPDFService

@login_required
def payslip_pdf(request, employee_id):

    return PayrollPDFService.generate_payslip(employee_id)


@login_required
def salary_download_csv(request):

    return ExportService.generate_salary_csv(request)


@login_required
def salary_download_pdf(request):

    return PayrollPDFService.generate_salary_report(request)