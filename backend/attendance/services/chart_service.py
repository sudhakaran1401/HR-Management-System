import calendar
from collections import Counter
from datetime import date
from attendance.services.record_service import AttendanceRecordService
from attendance.services.report_service import AttendanceReportService

class AttendanceChartService:

    @staticmethod
    def generate_chart_data(request):

        user = request.user

        year = request.GET.get("year")

        month = request.GET.get("month")

        employee_id = request.GET.get("employee")

        if not (year or month):

            return [0, 0, 0]

        year = int(year) if year else date.today().year

        month = int(month) if month else None

        records, _ = AttendanceReportService.get_monthly_attendance_stats(user, year, month, employee_id)

        # Date range
        if month:

            start_date = date(year, month, 1)

            end_date = date( year, month, calendar.monthrange(year, month)[1])

        else:

            start_date = date(year, 1, 1)

            end_date = date(year, 12, 31)

        processed_records = AttendanceRecordService.build_processed_records(
                            user=user,
                            records=records,
                            start_date=start_date,
                            end_date=end_date,
                            employee_id=employee_id
                        )

        counter = Counter([r.status for r in processed_records])

        return [
            counter.get("Present", 0),
            counter.get("Leave", 0),
            counter.get("Holiday", 0)
        ]