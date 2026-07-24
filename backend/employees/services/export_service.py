import csv
from django.http import HttpResponse

from utils.pdf_generate import render_pdf_report

class ExportService:

    @staticmethod
    def export_csv(filename, headers, rows):

        response = HttpResponse( content_type='text/csv' )

        response[ 'Content-Disposition' ] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)

        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

        return response
    

    @staticmethod
    def export_pdf( filename, month, year, dept_counts, headers, rows ):

        response = HttpResponse( content_type='application/pdf' )

        response[ 'Content-Disposition' ] = f'attachment; filename="{filename}"'

        return render_pdf_report(
            response,
            month=month,
            year=year,
            employee_name=None,
            title="Employee Report",
            summary_labels=list(dept_counts.keys()),
            summary_values=list(dept_counts.values()),
            table_title="Employee Details",
            table_headers=headers,
            table_rows=rows
        )