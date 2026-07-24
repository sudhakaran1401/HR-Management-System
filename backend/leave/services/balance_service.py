from django.db.models import Count, Q

from leave.models import LeaveRequest
from leave.constants import LeaveStatus, LeaveType, LeaveLimits

class BalanceService:

    @staticmethod
    def get_leave_balance(employee):

        queryset = LeaveRequest.objects.filter( employee=employee )

        counts = queryset.aggregate(

            total=Count("id"),

            approved=Count( "id", filter=Q(status=LeaveStatus.APPROVED) ),

            pending=Count( "id", filter=Q(status=LeaveStatus.PENDING) ),

            rejected=Count( "id", filter=Q(status=LeaveStatus.REJECTED) ),
        )

        approved_leaves = queryset.filter( status=LeaveStatus.APPROVED )

        leave_totals = {
            LeaveType.SICK: 0,
            LeaveType.CASUAL: 0,
            LeaveType.ANNUAL: 0,
        }

        for leave in approved_leaves:

            days = ( leave.end_date - leave.start_date ).days + 1

            if leave.leave_type in leave_totals:
               leave_totals[leave.leave_type] += days

        total_applied = sum( leave_totals.values() )

        total_max = ( LeaveLimits.SICK + LeaveLimits.CASUAL + LeaveLimits.ANNUAL )

        return {

            "total": counts["total"],
            "approved": counts["approved"],
            "pending": counts["pending"],
            "rejected": counts["rejected"],
            "sick_applied": leave_totals[LeaveType.SICK],
            "casual_applied": leave_totals[LeaveType.CASUAL],
            "annual_applied": leave_totals[LeaveType.ANNUAL],
            "total_applied": total_applied,
            "SICK_MAX": LeaveLimits.SICK,
            "CASUAL_MAX": LeaveLimits.CASUAL,
            "ANNUAL_MAX": LeaveLimits.ANNUAL,
            "TOTAL_MAX": total_max,
        }