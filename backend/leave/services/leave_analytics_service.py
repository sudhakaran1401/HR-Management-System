from django.db.models import Count, Q

from leave.constants import LeaveStatus


class LeaveAnalyticsService:

    @staticmethod
    def get_status_summary(queryset):

        return queryset.aggregate(

            total=Count("id"),

            approved=Count( "id", filter=Q(status=LeaveStatus.APPROVED) ),

            pending=Count( "id", filter=Q(status=LeaveStatus.PENDING) ),

            rejected=Count( "id", filter=Q(status=LeaveStatus.REJECTED) ),
        )