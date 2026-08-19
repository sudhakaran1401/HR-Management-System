from rest_framework import serializers
from payroll.models import SalaryHistory


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryHistory
        fields = "__all__"