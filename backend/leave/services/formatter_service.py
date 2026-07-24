from employees.models import Employee

class LeaveFormatterService:

    @staticmethod
    def get_report_headers():

        return [
            "Employee",
            "Department",
            "Leave Type",
            "Days",
            "Start Date",
            "End Date",
            "Reason",
            "Applied Date",
            "Status"
        ]
    
    @staticmethod
    def get_employee_name(employee_id):

        if not employee_id:
            return None

        employee = Employee.objects.filter( id=employee_id ).first()

        if employee:
            return employee.name

        return None

    @staticmethod
    def build_rows(queryset, format_type="csv"):

        rows = []

        for leave in queryset:

            applied_date = "-"

            if leave.applied_at:

                if format_type == "pdf":
                    applied_date = leave.applied_at.strftime( "%d %b %Y" )

                else:
                    applied_date = leave.applied_at.strftime( "%d-%m-%Y" )

            leave_type = ( leave.leave_type if format_type == "pdf" else leave.get_leave_type_display() )

            rows.append([
                leave.employee.name,
                leave.employee.department,
                leave_type,
                leave.total_days,
                str(leave.start_date),
                str(leave.end_date),
                leave.reason or "-",
                applied_date,
                leave.status
            ])

        return rows