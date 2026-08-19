from rest_framework import serializers
from leave.api.serializers import LeaveRequestSerializer

class EmployeeDashboardSerializer(serializers.Serializer):

    my_attendance_month = serializers.IntegerField()

    attendance_month_labels = serializers.ListField(
        child=serializers.CharField()
    )

    attendance_month_data = serializers.ListField(
        child=serializers.IntegerField()
    )

    leave_balance = serializers.IntegerField()

    my_approved_leaves = LeaveRequestSerializer( many=True )
    
    payroll_month_labels = serializers.ListField(
        child=serializers.CharField()
    )

    payroll_month_data = serializers.ListField(
        child=serializers.FloatField()
    )

    salary_count = serializers.IntegerField()

    latest_salary = serializers.JSONField()


class HRDashboardSerializer(serializers.Serializer):

    total_employees = serializers.IntegerField()

    pending_leaves = serializers.IntegerField()

    approved_leaves = serializers.IntegerField()

    rejected_leaves = serializers.IntegerField()

    today_attendance = serializers.IntegerField()

    present_count = serializers.IntegerField()

    absent_count = serializers.IntegerField()

    attendance_labels = serializers.ListField(
        child=serializers.CharField()
    )

    attendance_counts = serializers.ListField(
        child=serializers.IntegerField()
    )

    payroll_records_this_month = serializers.IntegerField()

    payroll_labels = serializers.ListField(
        child=serializers.CharField()
    )

    payroll_totals = serializers.ListField(
        child=serializers.FloatField()
    )

    dept_labels = serializers.ListField(
        child=serializers.CharField()
    )

    dept_counts = serializers.ListField(
        child=serializers.IntegerField()
    )

