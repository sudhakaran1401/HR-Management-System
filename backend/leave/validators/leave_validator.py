from leave.models import LeaveRequest
from attendance.models import Attendance
from attendance.constants import AttendanceStatus 

class LeaveValidator:
    @staticmethod
    def validate_leave_dates(start_date, end_date):

        if start_date > end_date:
            return False, "Start date cannot be after end date."

        return True, None

    @staticmethod
    def check_leave_overlap( employee, start_date, end_date, exclude_id=None ):

        queryset = LeaveRequest.objects.filter( employee=employee, start_date__lte=end_date, end_date__gte=start_date )

        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)

        if queryset.exists():
            return False, "Leave overlaps with existing request."

        return True, None
    
    @staticmethod
    def validate_attendance_conflict( employee, start_date, end_date ):

        attendance_exists = Attendance.objects.filter( 
            employee=employee, 
            date__range=[start_date, end_date],
            status=AttendanceStatus.PRESENT 
        ).exists()

        if attendance_exists:

            return ( False, "Attendance already marked as Present on these dates" )
        
        return True, None