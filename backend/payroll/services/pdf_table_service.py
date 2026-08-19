from reportlab.lib import colors
from reportlab.platypus import  Table, TableStyle


class PDFTableService:
    @staticmethod
    def build_employee_info_table(salary):

        info_data = [
            ["Employee ID", salary.employee.id, "Bank Name", "HDFC Bank"],
            ["Name", salary.employee.name, "Account No", "XXXX1234"],
            ["Department", salary.employee.department, "IFSC", "HDFC0001234"],
            ["Designation", salary.employee.designation, "PAN", "ABCDE1234F"],
        ]

        table = Table(info_data, colWidths=[120, 150, 120, 150])

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                    ("BACKGROUND", (2, 0), (2, -1), colors.lightgrey),
                ]
            )
        )

        return table

    @staticmethod
    def build_salary_table(salary):

        salary_data = [
            ["Earnings", "Amount", "Deductions", "Amount"],
            ["Basic", salary.basic, "PF", salary.pf],
            ["HRA", salary.hra, "Tax", salary.tax],
            ["Allowances", salary.allowances, "Other", salary.other_deductions],
            ["Gross", salary.gross, "Total Deduction", salary.total_deductions],
            ["NET PAY", salary.net_pay, "", ""],
        ]

        table = Table(salary_data, colWidths=[120, 100, 120, 100])

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("BACKGROUND", (0, -1), (1, -1), colors.white),
                    ("SPAN", (2, -1), (3, -1)),
                ]
            )
        )

        return table

    @staticmethod
    def build_attendance_table():

        attendance_data = [
            ["Working Days", "30"],
            ["Paid Days", "28"],
            ["LOP", "2"],
        ]

        table = Table(attendance_data, colWidths=[200, 200])

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ]
            )
        )

        return table

    @staticmethod
    def build_signature_table():

        table = Table(
            [["Employer Signature", "", "Employee Signature"]], colWidths=[180, 60, 180]
        )

        table.setStyle(
            TableStyle(
                [
                    ("LINEABOVE", (0, 0), (0, 0), 0.5, colors.black),
                    ("LINEABOVE", (2, 0), (2, 0), 0.5, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        return table

    @staticmethod
    def build_summary_table(summary):

        card_data = [
            ["Total Payrolls", summary["total_payrolls"]],
            ["Total Net Pay", f"₹ {summary['total_net_pay']}"],
        ]

        table = Table(card_data, colWidths=[250, 150])

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("BOX", (0, 0), (-1, -1), 1, colors.black),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ]
            )
        )

        return table

    
    @staticmethod
    def build_report_table(qs):

        table_data = [
            [
                "Employee",
                "Department",
                "Month",
                "Gross",
                "Deduction",
                "Net Pay",
                "Paid Date",
            ]
        ]

        for r in qs:
            table_data.append(
                [
                    r.employee.name,
                    r.employee.department,
                    r.pay_month.strftime("%b %Y"),
                    r.gross,
                    r.total_deductions,
                    r.net_pay,
                    (r.paid_date.strftime("%d %b %Y") if r.paid_date else "-"),
                ]
            )

        table = Table(table_data, repeatRows=1)

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BOX", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        return table