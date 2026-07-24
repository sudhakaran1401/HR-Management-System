from employees.services.analytics_service import EmployeeAnalyticsService
from employees.services.report_service import EmployeeReportService
from utils.file_name import generate_filename


class EmployeeReportBuilder:

    @staticmethod
    def rows(qs):

        rows = []

        for e in qs:

            rows.append([
                e.name,
                e.email,
                e.phone,
                e.department,
                e.designation,
                e.joining_date
            ])

        return rows

    @staticmethod
    def build_joining_report(month, year):

        employees = EmployeeReportService.filter_by_joining( month, year )

        headers = [
            "Name",
            "Email",
            "Phone",
            "Department",
            "Designation",
            "Joining Date"
        ]

        rows = EmployeeReportBuilder.rows(employees)

        dept_counts = ( EmployeeAnalyticsService.get_department_summary( employees ) )

        return {
            "employees": employees,
            "headers": headers,
            "rows": rows,
            "dept_counts": dept_counts,
            "csv_filename": generate_filename( "Employee Report", year, month, None, "csv" ),
            "pdf_filename": generate_filename( "Employee Report", year, month, None, "pdf" )
        }
    
    