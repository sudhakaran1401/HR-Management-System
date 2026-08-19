import calendar
import re
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, Spacer


class PDFHelperService:    
    @staticmethod
    def build_header(title):

        styles = getSampleStyleSheet()

        center_style = ParagraphStyle(
            name="Center", parent=styles["Normal"], alignment=TA_CENTER
        )

        title_style = ParagraphStyle(
            name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER
        )

        return [
            Paragraph("<b>YOUR COMPANY PVT LTD</b>", title_style),
            Paragraph("Chennai, Tamil Nadu", center_style),
            Spacer(1, 10),
            Paragraph(f"<b>{title}</b>", center_style),
            Spacer(1, 20),
        ]
    
    @staticmethod
    def build_chart(buffer):

        return Image(buffer, width=500, height=250)
    

    @staticmethod
    def build_payslip_filename(salary):

        salary_month = salary.pay_month.strftime("%b_%Y")

        employee_name = salary.employee.name.replace(" ", "_")

        return f"Payslip_{employee_name}_{salary_month}.pdf"

    @staticmethod
    def build_report_filename(title):

        file_title = title.replace(" ", "_")

        file_title = re.sub(r"[^a-zA-Z0-9_]", "", file_title)

        return f"{file_title}.pdf"

    @staticmethod
    def build_report_title(request, qs):

        employee_id = request.GET.get("employee")
        month = request.GET.get("month")
        year = request.GET.get("year")

        employee_name = None

        if employee_id:
            record = qs.filter(employee__id=employee_id).first()

            if record:
                employee_name = record.employee.name

        if not employee_name:
            employee_name = "All Employees"

        if month and month.isdigit():
            month_name = calendar.month_name[int(month)]
        else:
            month_name = month

        title = "Payroll Report"

        if employee_name != "All Employees" and month_name and year:
            title += f" - {employee_name} ({month_name} {year})"

        elif employee_name != "All Employees" and year:
            title += f" - {employee_name} ({year})"

        elif employee_name != "All Employees":
            title += f" - {employee_name}"

        elif month_name and year:
            title += f" - {month_name} {year}"

        elif year:
            title += f" - {year}"

        else:
            title += " - All Employees"

        return title
