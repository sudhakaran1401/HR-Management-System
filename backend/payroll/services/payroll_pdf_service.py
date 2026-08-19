from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from payroll.models import SalaryHistory
from utils.filters import apply_common_filters
from payroll.services.chart_service import PayrollChartService
from payroll.services.summary_service import PayrollSummaryService
from payroll.services.pdf_helper_service import PDFHelperService
from payroll.services.pdf_table_service import PDFTableService


class PayrollPDFService:
    @staticmethod
    def generate_payslip(employee_id):

        salary = SalaryHistory.objects.select_related("employee").get(pk=employee_id)

        response = HttpResponse(content_type="application/pdf")

        response["Content-Disposition"] = (
            f'attachment; filename="'
            f'{PDFHelperService.build_payslip_filename(salary)}"'
        )

        doc = SimpleDocTemplate(response, pagesize=A4)

        elements = []

        elements.extend(
            PDFHelperService.build_header(
                f"Salary Slip - {salary.pay_month.strftime('%B %Y')}"
            )
        )

        elements.append(PDFTableService.build_employee_info_table(salary))

        elements.append(Spacer(1, 20))

        elements.append(PDFTableService.build_salary_table(salary))

        elements.append(Spacer(1, 20))

        elements.append(PDFTableService.build_attendance_table())

        elements.append(Spacer(1, 30))

        styles = getSampleStyleSheet()

        elements.append(
            Paragraph("Note: This is a system-generated payslip.", styles["Normal"])
        )

        elements.append(Spacer(1, 30))

        elements.append(PDFTableService.build_signature_table())

        doc.build(elements)

        return response

    @staticmethod
    def generate_salary_report(request):

        qs = apply_common_filters(
            SalaryHistory.objects.select_related("employee"), request, "pay_month"
        )

        title_text = PDFHelperService.build_report_title(request, qs)

        summary = PayrollSummaryService.get_summary(qs)

        chart_data = (
            qs.annotate(month=TruncMonth("pay_month"))
            .values("month")
            .annotate(total_net=Sum("stored_net_pay"))
            .order_by("month")
        )

        months = [d["month"].strftime("%b %Y") for d in chart_data]

        totals = [float(d["total_net"]) for d in chart_data]

        chart_buffer = PayrollChartService.generate_salary_chart(months, totals)

        response = HttpResponse(content_type="application/pdf")

        response["Content-Disposition"] = (
            f'attachment; filename="'
            f'{PDFHelperService.build_report_filename(title_text)}"'
        )

        doc = SimpleDocTemplate(response)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph(f"<b>{title_text}</b>", styles["Title"]))

        elements.append(Spacer(1, 15))

        elements.append(PDFTableService.build_summary_table(summary))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph("<b>Salary Chart</b>", styles["Heading2"]))

        elements.append(Spacer(1, 10))

        elements.append(PDFHelperService.build_chart(chart_buffer))

        elements.append(Spacer(1, 20))

        elements.append(PDFTableService.build_report_table(qs))

        doc.build(elements)

        return response


