from leave.services.leave_analytics_service import LeaveAnalyticsService

from leave.services.formatter_service import LeaveFormatterService 

from leave.selectors.leave_selectors import LeaveSelector

from utils.file_name import generate_filename


class LeaveReportBuilder:

    @staticmethod
    def build(month=None, year=None, employee_id=None):

        queryset = LeaveSelector.filtered_leave_queryset( month=month, year=year, employee_id=employee_id, ) 

        summary =  LeaveAnalyticsService.get_status_summary( queryset )

        headers = LeaveFormatterService.get_report_headers() 

        rows = LeaveFormatterService.build_rows( queryset ) 

        employee_name = LeaveFormatterService.get_employee_name( employee_id ) 

        return {

            "queryset": queryset,

            "summary": summary,

            "headers": headers,

            "rows": rows,

            "employee_name": employee_name,

            "csv_filename": generate_filename( "Leave Report", year, month, employee_name, "csv", ),

            "pdf_filename": generate_filename( "Leave Report", year, month, employee_name, "pdf", )
        }