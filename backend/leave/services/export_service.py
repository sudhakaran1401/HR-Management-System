import csv
from django.http import HttpResponse
from utils.pdf_generate import render_pdf_report

class ExportService:

    @staticmethod
    def export_csv(filename, headers, rows):

        response = HttpResponse( content_type="text/csv" )

        response[ "Content-Disposition" ] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)

        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

        return response

    @staticmethod
    def export_pdf( filename, month, year, employee_name, summary, headers, rows, ):

        response = HttpResponse( content_type="application/pdf" )

        response[ "Content-Disposition" ] = f'attachment; filename="{filename}"'

        return render_pdf_report(
            response,
            title="Leave Report",
            summary_labels=[
                "Applied",
                "Approved",
                "Pending",
                "Rejected",
            ],
            summary_values=[
                summary["total"],
                summary["approved"],
                summary["pending"],
                summary["rejected"],
            ],
            table_title="Leave Details",
            table_headers=headers,
            table_rows=rows,
            month=month,
            year=year,
            employee_name=employee_name,
        )